"""guards/verify_on_stop — turn-end verification guard for double_checking.

Pattern ported from Hermes ``agent/verification_stop.py`` (MIT). This module is
intentionally **policy-only**: it turns a passive verification ledger into a
bounded follow-up when the model tries to finish without fresh evidence.

For ProgressiveAgentSLM, "evidence" is retrieval results / delegate outputs, not
code edits. The guard becomes: if the model tries to emit a final answer and the
answer evaluator says the evidence doesn't cover the question, the loop should
continue one more bounded round (while ``CircularRounds.remaining > 0``).

The doc/markdown skip is the ported insight: a turn that only wrote ``todo.md``
or a Mermaid ``.md`` must never demand a verification round.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, List

# Extensions whose edits carry no verifiable runtime behavior — documentation,
# prose, and data/markup that no test/build exercises.
_NON_CODE_VERIFY_EXTENSIONS = frozenset({
    ".md", ".markdown", ".mdx", ".rst", ".txt", ".text", ".adoc", ".asciidoc",
    ".org", ".log", ".csv", ".tsv",
})

# Filenames (extension-less or otherwise) that are pure prose.
_NON_CODE_VERIFY_FILENAMES = frozenset({
    "license", "licence", "notice", "authors", "contributors", "changelog",
    "codeowners",
})


def _is_non_code_path(raw: str) -> bool:
    try:
        p = Path(str(raw))
    except Exception:
        return False
    suffix = p.suffix.lower()
    if suffix in _NON_CODE_VERIFY_EXTENSIONS:
        return True
    if not suffix and p.name.lower() in _NON_CODE_VERIFY_FILENAMES:
        return True
    return False


def filter_verifiable_paths(paths: Iterable[str]) -> List[str]:
    """Drop doc/prose paths; keep paths that could have verifiable behavior."""
    return [p for p in paths if p and not _is_non_code_path(p)]


def should_nudge_on_stop(
    *,
    changed_paths: List[str],
    evidence_covers_question: bool,
    rounds_remaining: int,
) -> bool:
    """Return whether to inject one more bounded round before a final answer.

    Nudge (true) when:
      - there were verifiable (non-prose) artifacts changed, AND
      - the evidence does NOT cover the question, AND
      - a bounded round remains.
    The doc/markdown skip means a turn that touched only prose (e.g. only
    ``todo.md``) never nudges.
    """
    verifiable = filter_verifiable_paths(changed_paths)
    if not verifiable:
        return False
    if evidence_covers_question:
        return False
    if rounds_remaining <= 0:
        return False
    return True


def verify_on_stop_message(
    *,
    changed_paths: List[str],
    evidence_covers_question: bool,
    rounds_remaining: int,
    rounds_max: int,
) -> str | None:
    """Human-readable guidance string, or ``None`` if no nudge is warranted."""
    if not should_nudge_on_stop(
        changed_paths=changed_paths,
        evidence_covers_question=evidence_covers_question,
        rounds_remaining=rounds_remaining,
    ):
        return None
    shown = ", ".join(filter_verifiable_paths(changed_paths)[:5])
    return (
        f"Evidence does not yet cover the question (artifacts: {shown}). "
        f"Run one more bounded retrieval round ({rounds_remaining}/{rounds_max} left)."
    )


def evidence_verdict_from_notes(notes: Any) -> bool:
    """Best-effort: extract an evidence-covers-question bool from evaluator notes.

    Accepts a dict (``{"covers_question": bool}``) or a float/str threshold.
    Defaults to True (assume covered) so a missing signal never spams nudges.
    """
    if isinstance(notes, dict):
        val = notes.get("covers_question")
        if isinstance(val, bool):
            return val
    return True