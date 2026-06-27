"""Worklog — per-run shared compact memory file.

Every delegate (agent / tool / knowledge source) appends a concise summary
of its contribution.  The Reflector rewrites the whole file after each step
to keep it small, non-redundant, and current.

One instance lives per run, owned by RunLogger.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone


class Worklog:
    """Thin wrapper around runs/<run_id>/worklog.md."""

    def __init__(self, run_dir: str) -> None:
        self._path = os.path.join(run_dir, "worklog.md")
        os.makedirs(run_dir, exist_ok=True)
        if not os.path.exists(self._path):
            ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
            with open(self._path, "w", encoding="utf-8") as fh:
                fh.write(f"# Worklog\n\n_Created: {ts}Z_\n\n")

    @property
    def path(self) -> str:
        return self._path

    def read(self) -> str:
        with open(self._path, "r", encoding="utf-8") as fh:
            return fh.read()

    def append(self, section: str, compact: str) -> None:
        """Append a compact entry under a timestamped section heading."""
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        entry = f"\n## {section}\n_({ts}Z)_\n\n{compact.strip()}\n"
        with open(self._path, "a", encoding="utf-8") as fh:
            fh.write(entry)

    def revise(self, revised_content: str) -> None:
        """Replace the entire worklog with a reflection-revised version."""
        with open(self._path, "w", encoding="utf-8") as fh:
            fh.write(revised_content.strip() + "\n")

    def char_count(self) -> int:
        return len(self.read())
