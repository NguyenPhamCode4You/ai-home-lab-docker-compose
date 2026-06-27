"""RunLogger — per-run structured logger.

Creates three artefacts inside runs/<run_id>/:

  events.jsonl    — append-only JSONL event stream (every think/act/delegate/reflect)
  transcript.md   — full human-readable verbatim rendering
  worklog.md      — compact, reflection-revised shared memory (via Worklog)

Event schema (each line of events.jsonl)::

    {
      "run_id":   "8-char hex",
      "ts":       "ISO-8601Z",
      "step_id":  "node id or 'root'",
      "phase":    "plan|act|observe|reflect|delegate|worklog|final",
      "actor":    "forwarder|reflector|tool:NAME|agent:NAME|...",
      "input":    "prompt / action args (truncated to 500 chars)",
      "output":   "result / summary (truncated to 500 chars)",
      "status":   "ok|error|skipped",
      "tokens":   0
    }
"""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone

from ..Worklog import Worklog


class RunLogger:
    """Owns the run directory and all three logging artefacts."""

    def __init__(self, runs_dir: str = "runs") -> None:
        self.run_id = uuid.uuid4().hex[:8]
        self.run_dir = os.path.join(runs_dir, self.run_id)
        os.makedirs(self.run_dir, exist_ok=True)

        self._events_path = os.path.join(self.run_dir, "events.jsonl")
        self._transcript_path = os.path.join(self.run_dir, "transcript.md")
        self.worklog = Worklog(self.run_dir)

        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with open(self._transcript_path, "w", encoding="utf-8") as fh:
            fh.write(f"# Run {self.run_id}\n\n_Started: {ts}Z_\n\n---\n\n")

        print(f"[RunLogger] run_id={self.run_id}  dir={self.run_dir}", flush=True)

    # ── Events ─────────────────────────────────────────────────────────────

    def log_event(
        self,
        step_id: str,
        phase: str,
        actor: str,
        input_text: str = "",
        output_text: str = "",
        status: str = "ok",
        tokens: int = 0,
    ) -> None:
        event = {
            "run_id": self.run_id,
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds") + "Z",
            "step_id": step_id,
            "phase": phase,
            "actor": actor,
            "input": str(input_text)[:500],
            "output": str(output_text)[:500],
            "status": status,
            "tokens": tokens,
        }
        with open(self._events_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(event) + "\n")

    # ── Transcript ─────────────────────────────────────────────────────────

    def append_transcript(self, text: str) -> None:
        with open(self._transcript_path, "a", encoding="utf-8") as fh:
            fh.write(text)

    def echo(self, text: str) -> None:
        """Print to terminal and append to transcript simultaneously."""
        print(text, end="", flush=True)
        self.append_transcript(text)
