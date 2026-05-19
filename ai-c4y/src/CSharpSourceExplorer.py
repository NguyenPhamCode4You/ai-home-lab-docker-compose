"""
CSharpSourceExplorer.py

An assistant that answers questions about a C# codebase by directly reading the
most relevant source files and sending them to Claude Sonnet — no vector database
or pre-indexing required.

File selection strategy (single-pass, no subprocess):
  - Walks all .cs files under CIA_CODEBASE_PATH (respects CIA_IGNORE_FILES)
  - Scores each file by keyword match in filename/path (high signal) and in
    file content up to first 50 KB (lower signal)
  - Returns the top N files by score (N = CIA_EXPLORER_MAX_FILES, default 20)

Streaming contract (matches ChatBackend.create_chat_backend):
  async def stream(question, context, conversation_history) -> AsyncGenerator[str, None]
"""

import asyncio
import os
import re
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from .agents.models.OpenRouter import OpenRouter
from .cia_config import CSHARP_CODEBASE_PATH, CSHARP_IGNORE_FILES

load_dotenv()

_MODEL          = os.getenv("CIA_EXPLORER_MODEL",      "anthropic/claude-sonnet-4.6")
_MAX_FILES      = int(os.getenv("CIA_EXPLORER_MAX_FILES",      "20"))
_MAX_FILE_CHARS = int(os.getenv("CIA_EXPLORER_MAX_FILE_CHARS", "15000"))

_SYSTEM_PROMPT = """\
You are a senior software engineer with deep expertise in the BVMS (BBC Voyage Management System) C# backend codebase.
You have been provided the raw source code of the most relevant C# files to answer the user's question.

{histories}\
User question: {question}

Source files retrieved from the codebase:
{files_context}

Answer guidelines:
- Cite the exact file path, class name, and method signature when referencing code.
- For business logic questions: explain the WHY and WHEN — the domain reasoning behind the design.
- For dependency questions: trace the call chain and identify callers/dependents.
- For workflow questions: walk through the execution path step by step.
- If the provided files do not contain enough information, say so clearly and state what is known.
- Use BVMS-specific terminology (TCO, BDN, voyage reconciliation, etc.) as found in the source.
- Do not invent class names or business rules not present in the provided files.
- Use markdown diagrams to illustrate workflows or class relationships when relevant.
"""

# Stop words excluded from keyword extraction
_STOP_WORDS = {
    "the", "how", "does", "what", "is", "are", "where", "when", "why", "which",
    "can", "and", "for", "to", "in", "of", "a", "an", "do", "get", "set",
    "show", "me", "this", "that", "with", "from", "on", "at", "by", "be",
    "has", "was", "will", "all", "have", "not", "but", "its", "if", "or",
    "any", "use", "used", "called", "call", "return", "returns",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_ignore_patterns(ignore_str: str) -> list[str]:
    return [p.strip() for p in ignore_str.split(",") if p.strip()]


def _is_ignored(rel_path: str, patterns: list[str]) -> bool:
    p = rel_path.replace("\\", "/")
    for pat in patterns:
        pat_norm = pat.strip().replace("\\", "/")
        regex = re.escape(pat_norm).replace(r"\*\*", ".*").replace(r"\*", "[^/]*").replace(r"\?", "[^/]")
        if re.search(regex, p, re.IGNORECASE):
            return True
    return False


def _extract_keywords(question: str) -> list[str]:
    """Return unique tokens ≥ 3 chars that are not stop words."""
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9]+", question)
    seen: set[str] = set()
    result: list[str] = []
    for t in tokens:
        tl = t.lower()
        if tl not in _STOP_WORDS and len(tl) >= 3 and tl not in seen:
            seen.add(tl)
            result.append(t)
    return result


def _score_by_name(rel_path: str, keywords: list[str]) -> int:
    """Return keyword-match score based on filename and path segments."""
    stem = Path(rel_path).stem.lower()
    path_lower = rel_path.lower()
    score = 0
    for kw in keywords:
        kl = kw.lower()
        if kl in stem:
            score += 3          # direct class-name hit
        elif kl in path_lower:
            score += 1          # directory/path hit
    return score


def _get_chat_history_string(conversation_history: list, max_chars: int = 6000) -> str:
    """Format the last N chars of conversation history, excluding the current user turn."""
    if not conversation_history:
        return ""

    lines: list[str] = []
    total = 0

    # Walk backwards, skip the last user message (it's already in `question`)
    messages = conversation_history[:-1]
    for msg in reversed(messages):
        if isinstance(msg, dict):
            role = msg.get("role", "user")
            content = msg.get("content", "")
        else:
            role = getattr(msg, "role", "user")
            content = getattr(msg, "content", "")

        entry = f"{role.upper()}: {content[-2000:]}"
        if total + len(entry) > max_chars:
            break
        lines.insert(0, entry)
        total += len(entry)

    if not lines:
        return ""
    return "Conversation history:\n" + "\n\n".join(lines) + "\n\n"


# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------

class CSharpSourceExplorer:
    """
    Stateless assistant: given a user question, selects the most relevant .cs
    files from the codebase, assembles them into a prompt, and streams the
    Claude Sonnet answer back to the caller.
    """

    def __init__(
        self,
        codebase_path: str | None = None,
        model: str | None = None,
        max_files: int | None = None,
        max_file_chars: int | None = None,
    ):
        self.codebase_path  = codebase_path or CSHARP_CODEBASE_PATH
        self.llm            = OpenRouter(model=model or _MODEL)
        self.max_files      = max_files      or _MAX_FILES
        self.max_file_chars = max_file_chars or _MAX_FILE_CHARS
        self._ignore        = _build_ignore_patterns(CSHARP_IGNORE_FILES)

    # ------------------------------------------------------------------
    # File selection (runs in executor to avoid blocking the event loop)
    # ------------------------------------------------------------------

    def _scan_codebase(self, keywords: list[str]) -> list[tuple[str, int]]:
        """
        Synchronous scan — meant to be called via run_in_executor.
        Returns (rel_path, score) pairs sorted by descending score, capped at max_files.
        """
        kw_pattern = (
            re.compile("|".join(re.escape(k) for k in keywords[:15]), re.IGNORECASE)
            if keywords else None
        )
        scored: dict[str, int] = {}

        for root, dirs, files in os.walk(self.codebase_path):
            # Prune ignored subdirectories early to speed up traversal
            dirs[:] = [
                d for d in dirs
                if not _is_ignored(
                    os.path.relpath(os.path.join(root, d), self.codebase_path).replace("\\", "/") + "/",
                    self._ignore,
                )
            ]

            for fname in files:
                if not fname.endswith(".cs"):
                    continue

                rel = os.path.relpath(
                    os.path.join(root, fname), self.codebase_path
                ).replace("\\", "/")

                if _is_ignored(rel, self._ignore):
                    continue

                name_score    = _score_by_name(rel, keywords)
                content_score = 0

                if kw_pattern:
                    try:
                        with open(os.path.join(self.codebase_path, rel),
                                  "r", encoding="utf-8", errors="replace") as fh:
                            sample = fh.read(51_200)   # scan first 50 KB only
                        if kw_pattern.search(sample):
                            content_score = 2
                    except OSError:
                        pass

                total = name_score + content_score
                if total > 0:
                    scored[rel] = total

        ranked = sorted(scored.items(), key=lambda x: (-x[1], x[0]))
        return ranked[: self.max_files]

    async def _select_files(self, question: str) -> list[tuple[str, int]]:
        keywords = _extract_keywords(question)
        if not keywords:
            return []
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._scan_codebase, keywords)

    # ------------------------------------------------------------------
    # File reading
    # ------------------------------------------------------------------

    def _read_file(self, rel_path: str) -> str:
        full_path = os.path.join(self.codebase_path, rel_path)
        try:
            size = os.path.getsize(full_path)
            with open(full_path, "r", encoding="utf-8", errors="replace") as fh:
                content = fh.read(self.max_file_chars)
            if size > self.max_file_chars:
                content += f"\n\n// ... [file truncated — {size - self.max_file_chars:,} chars omitted]"
            return content
        except OSError:
            return ""

    # ------------------------------------------------------------------
    # Public streaming interface (required by ChatBackend)
    # ------------------------------------------------------------------

    async def stream(
        self,
        question: str | None = None,
        context: str | None = None,
        conversation_history: list | None = None,
    ):
        if not question:
            yield "No question provided."
            return

        if not self.codebase_path or not os.path.isdir(self.codebase_path):
            yield (
                f"❌ **Codebase path is not set or does not exist:** `{self.codebase_path}`\n\n"
                "Set the `CIA_CODEBASE_PATH` environment variable to the root of the C# project."
            )
            return

        yield "🔍 Scanning codebase for relevant files...\n\n"

        ranked = await self._select_files(question)

        if not ranked:
            yield (
                "⚠️ **No relevant `.cs` files found.** "
                "Try rephrasing with more specific class or method names.\n"
            )
            return

        yield f"📂 **{len(ranked)} file(s) selected:**\n"
        for rel, score in ranked:
            yield f"- `{rel}` (relevance: {score})\n"
        yield "\n---\n\n"

        # Build the files context block sent to the LLM
        file_blocks: list[str] = []
        for rel, _ in ranked:
            content = self._read_file(rel)
            if content:
                file_blocks.append(f"### File: `{rel}`\n```csharp\n{content}\n```")

        if not file_blocks:
            yield "⚠️ Files were selected but could not be read. Check file permissions.\n"
            return

        files_context = "\n\n".join(file_blocks)
        histories     = _get_chat_history_string(conversation_history)

        prompt = _SYSTEM_PROMPT.format(
            question=question,
            files_context=files_context,
            histories=histories,
        )

        async for chunk in self.llm.stream(prompt):
            yield chunk
