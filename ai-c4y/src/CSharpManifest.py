import hashlib
import json
import os

from dotenv import load_dotenv

load_dotenv()

MANIFEST_FILE = os.getenv("CODE_IMPACT_ANALYZER_MANIFEST_PATH", "wip/csharp-manifest.json")

# Phase ordering for comparison
PHASE_ORDER = {
    "unprocessed": 0,
    "indexed": 1,
    "documented": 2,
    "enriched": 3,
    "synthesized": 4,
    "inserted": 5,
}


class CSharpManifest:
    """
    Utility class wrapping csharp-manifest.json.
    Tracks per-file processing phase, file hashes, and metadata across the pipeline.

    manifest.json structure:
    {
      "Core/Business/VoyageManagement/Voyage/GetVoyageById.cs": {
        "phase": "indexed",
        "hash": "abc123...",
        "processed_at": "2025-01-01T00:00:00",
        "lines": 45,
        "file_type": "Handler",
        "architecture_layer": "Business",
        "doc_path": "csharp-docs/raw/Core/Business/.../GetVoyageById.md",
        "is_critical": false
      },
      ...
    }
    """

    def __init__(self, manifest_path: str = None):
        self.manifest_path = manifest_path or MANIFEST_FILE
        self._data: dict = {}
        self.load()

    # ------------------------------------------------------------------
    # Load / Save
    # ------------------------------------------------------------------

    def load(self) -> dict:
        if os.path.exists(self.manifest_path):
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        else:
            self._data = {}
        return self._data

    def save(self):
        os.makedirs(os.path.dirname(os.path.abspath(self.manifest_path)), exist_ok=True)
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    # ------------------------------------------------------------------
    # Phase management
    # ------------------------------------------------------------------

    def get_phase(self, file_path: str) -> str | None:
        """Return the current phase of a file, or None if not tracked."""
        entry = self._data.get(file_path)
        return entry.get("phase") if entry else None

    def set_phase(self, file_path: str, phase: str, extra: dict = None):
        """Set the phase for a file and optionally merge additional metadata."""
        if file_path not in self._data:
            self._data[file_path] = {}
        self._data[file_path]["phase"] = phase
        if extra:
            self._data[file_path].update(extra)

    def get_all_at_phase(self, phase: str) -> list[str]:
        """Return all file paths currently at the given phase."""
        return [fp for fp, entry in self._data.items() if entry.get("phase") == phase]

    def get_all_at_or_after_phase(self, phase: str) -> list[str]:
        """Return all file paths at the given phase or any later phase."""
        threshold = PHASE_ORDER.get(phase, 0)
        return [
            fp for fp, entry in self._data.items()
            if PHASE_ORDER.get(entry.get("phase", "unprocessed"), 0) >= threshold
        ]

    def reset_file(self, file_path: str):
        """Reset a file back to 'unprocessed' (used by incremental mode)."""
        if file_path in self._data:
            self._data[file_path]["phase"] = "unprocessed"

    # ------------------------------------------------------------------
    # Entry access
    # ------------------------------------------------------------------

    def get(self, file_path: str) -> dict:
        """Return the full manifest entry for a file (or empty dict)."""
        return self._data.get(file_path, {})

    def all_entries(self) -> dict:
        """Return the entire manifest data dict."""
        return self._data

    # ------------------------------------------------------------------
    # Hash / change detection
    # ------------------------------------------------------------------

    def compute_hash(self, file_path: str) -> str:
        """Compute SHA-256 hash of a file's content."""
        with open(file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def has_changed(self, file_path: str) -> bool:
        """Return True if the file content differs from the stored hash."""
        stored_hash = self._data.get(file_path, {}).get("hash")
        if not stored_hash:
            return True
        try:
            return self.compute_hash(file_path) != stored_hash
        except FileNotFoundError:
            return True

    # ------------------------------------------------------------------
    # Dependency traversal (used by incremental mode)
    # ------------------------------------------------------------------

    def get_dependents(self, file_path: str, index: dict) -> list[str]:
        """
        Given a changed file's path, return all other files in the index
        that reference this file's class_name (via used_by reverse lookup).
        Used by --mode=incremental to expand the re-processing scope.
        """
        file_entry = index.get("files", {}).get(file_path, {})
        class_name = file_entry.get("class_name", "")
        if not class_name:
            return []
        return index.get("used_by", {}).get(class_name, [])

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def print_summary(self):
        counts = {}
        for entry in self._data.values():
            phase = entry.get("phase", "unknown")
            counts[phase] = counts.get(phase, 0) + 1
        print("[Manifest Summary]")
        for phase in ["unprocessed", "indexed", "documented", "enriched", "synthesized", "inserted"]:
            print(f"  {phase}: {counts.get(phase, 0)}")
        other = {k: v for k, v in counts.items() if k not in PHASE_ORDER}
        for k, v in other.items():
            print(f"  {k}: {v}")
