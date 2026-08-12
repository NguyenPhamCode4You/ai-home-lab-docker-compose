"""ModelChain — role-tagged models_ladder + model_selection.

Chooses the working reasoning model: ``model_selection == "auto"`` → the first
reachable ``is_general_purpose`` entry; a model ``name`` pins that entry. Each
model carries one per-model FAILOVER budget (``max_retries_until_switching_models``)
covering **both** quality self-eval and infra failures; success resets the ladder
to the selection. Platform factory maps ``ollama`` / ``lmstudio`` / ``open_router``.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


class ModelEntry:
    def __init__(self, cfg: Dict[str, Any]) -> None:
        self.platform: str = cfg.get("platform", "ollama")
        self.name: str = cfg.get("name", "")
        self.url: Optional[str] = cfg.get("url")
        self.max_tokens = cfg.get("max_tokens", "auto")  # int | "auto"
        self.keep_warm: bool = bool(cfg.get("keep_warm", False))
        self.max_concurrency: int = int(cfg.get("max_concurrency", 1))
        self.when: str = cfg.get("when", "")
        self.is_embedding = bool(cfg.get("is_embedding", False))
        self.is_tool_selection = bool(cfg.get("is_tool_selection", False))
        self.is_general_purpose = bool(cfg.get("is_general_purpose", False))
        self.is_memory_distillation = bool(cfg.get("is_memory_distillation", False))
        self.is_reflection_and_evaluation = bool(cfg.get("is_reflection_and_evaluation", False))
        self.is_coding = bool(cfg.get("is_coding", False))
        self.is_vision = bool(cfg.get("is_vision", False))
        self.is_multimodal = bool(cfg.get("is_multimodal", False))
        self.is_fallback = bool(cfg.get("is_fallback", False))

    def has_flag(self, flag: str) -> bool:
        return bool(getattr(self, "is_" + flag.replace("is_", ""), False))


class ModelChain:
    def __init__(
        self,
        ladder: List[Dict[str, Any]],
        model_selection: str = "auto",
        max_retries_until_switching_models: int = 5,
    ) -> None:
        self._entries: List[ModelEntry] = [ModelEntry(cfg) for cfg in ladder]
        self._selection = model_selection or "auto"
        self.max_retries = max_retries_until_switching_models or 5
        # Per-entry retry counters (quality + infra share ONE counter each).
        self._failures: Dict[str, int] = {}
        # Current active index; None = not yet selected.
        self._active_index: Optional[int] = None

    @property
    def entries(self) -> List[ModelEntry]:
        return self._entries

    def flag_positions(self, flag: str) -> List[int]:
        """Indices of entries carrying *flag* (in ladder order)."""
        return [i for i, e in enumerate(self._entries) if e.has_flag(flag)]

    def select(self, role: str = "general") -> Optional[ModelEntry]:
        """Pick the working model for a task *role*.

        ``role="general"``: model_selection "auto" → first reachable is_general_purpose;
        a pinned name → that entry. Other roles: first entry with the matching
        flag, else first general-purpose.
        """
        if role == "general":
            if self._selection != "auto":
                for e in self._entries:
                    if e.name == self._selection:
                        self._active_index = self._entries.index(e)
                        return e
            return self._pick_first("is_general_purpose")
        # Capability-routed (embedding / tool_selection / coding / ...).
        flag = "is_" + role
        idx = self._pick_first(flag)
        if idx is None:
            idx = self._pick_first("is_general_purpose")
        return idx

    def _pick_first(self, flag: str) -> Optional[ModelEntry]:
        for i, e in enumerate(self._entries):
            if e.has_flag(flag):
                self._active_index = i
                return e
        return None

    # ── Failover (Phase 0 checklist: items 10–15) ─────────────────────────

    def current(self) -> Optional[ModelEntry]:
        if self._active_index is None:
            # Default selection on first use.
            return self.select("general")
        return self._entries[self._active_index]

    def record_failure(self) -> bool:
        """Record a quality/infra failure on the active model.

        Returns True when the failure budget is exhausted and the ladder pointer
        has advanced (or the ladder is exhausted → caller should stop).
        """
        entry = self.current()
        if entry is None:
            return True
        key = f"{entry.platform}:{entry.name}"
        self._failures[key] = self._failures.get(key, 0) + 1
        if self._failures[key] >= self.max_retries:
            return self._advance()
        return False

    def record_success(self) -> None:
        """Success resets the ladder to the top (cheapest capable first)."""
        self._failures.clear()
        self._active_index = None

    def _advance(self) -> bool:
        """Move to the next general-purpose entry. True if exhausted."""
        if self._active_index is None:
            self._active_index = 0
        start = self._active_index
        i = self._active_index
        n = len(self._entries)
        # Next general-purpose (or fallback) after the current position.
        for _ in range(n):
            i = (i + 1) % n
            if i == start:
                self._failures.clear()
                return True  # exhausted — looped back to start
            if self._entries[i].is_general_purpose or self._entries[i].is_fallback:
                self._active_index = i
                self._failures.clear()
                return False
        return True

    def build_client(self, entry: ModelEntry) -> Any:
        """Platform factory → the matching model client (Phase 1 wiring)."""
        if entry.platform in ("ollama", "lmstudio"):
            from src.agents.models.Ollama import Ollama

            return Ollama(url=entry.url, model=entry.name)
        if entry.platform == "open_router":
            from src.agents.models.OpenRouter import OpenRouter

            return OpenRouter(model=entry.name)
        raise ValueError(f"Unknown platform {entry.platform!r}")