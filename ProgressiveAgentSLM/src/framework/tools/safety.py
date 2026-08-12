"""tools/safety — shared file-tool safety rules (traversal + deny-list).

Pattern ported from Hermes ``agent/file_safety.py`` (MIT). Two layers beyond
plain path-traversal rejection:

1. **Exact denied paths** — `.ssh/id_rsa`, `.env`, `.netrc`, `.pgpass`,
   `.npmrc`, `.pypirc`, `.git-credentials`, `/etc/sudoers`, `/etc/passwd`,
   `/etc/shadow`, …
2. **Denied directory prefixes** — `.ssh/`, `.aws/`, `.gnupg/`, `.kube/`,
   `.docker/`, `.azure/`, `.config/gh/`, `.config/gcloud/`, `/etc/sudoers.d/`,
   `/etc/systemd/`, …

These apply **even inside an allowed root**: a ``writable`` working directory must
not let the agent rewrite ``.env``. Safe roots (the run's ``base_folder_path`` +
any ``writable`` ``working_directories``) are passed in at construction; the
deny-list is applied to every resolved path.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Sequence, Set

# Basenames treated as .env files (used by redact.py too so the two defenses
# can't drift: if file_tools blocks a read and the agent falls back to `cat`,
# the terminal redactor still catches it).
_BLOCKED_PROJECT_ENV_BASENAMES = frozenset(
    {".env", ".env.local", ".env.production", ".env.development"}
)


def build_denied_paths(home: str) -> Set[str]:
    """Return exact sensitive paths that must never be read or written."""
    return {
        os.path.realpath(p)
        for p in [
            os.path.join(home, ".ssh", "authorized_keys"),
            os.path.join(home, ".ssh", "id_rsa"),
            os.path.join(home, ".ssh", "id_ed25519"),
            os.path.join(home, ".ssh", "config"),
            os.path.join(home, ".env"),
            os.path.join(home, ".netrc"),
            os.path.join(home, ".pgpass"),
            os.path.join(home, ".npmrc"),
            os.path.join(home, ".pypirc"),
            os.path.join(home, ".git-credentials"),
            "/etc/sudoers",
            "/etc/passwd",
            "/etc/shadow",
        ]
    }


def build_denied_prefixes(home: str) -> list:
    """Return sensitive directory prefixes that must never be touched."""
    return [
        os.path.realpath(p) + os.sep
        for p in [
            os.path.join(home, ".ssh"),
            os.path.join(home, ".aws"),
            os.path.join(home, ".gnupg"),
            os.path.join(home, ".kube"),
            "/etc/sudoers.d",
            "/etc/systemd",
            os.path.join(home, ".docker"),
            os.path.join(home, ".azure"),
            os.path.join(home, ".config", "gh"),
            os.path.join(home, ".config", "gcloud"),
        ]
    ]


def is_path_denied(path: str, denied_paths: Set[str], denied_prefixes: Sequence[str]) -> bool:
    """Return True when *path* hits the exact deny-list or a denied prefix."""
    resolved = os.path.realpath(os.path.expanduser(str(path)))
    if resolved in denied_paths:
        return True
    for prefix in denied_prefixes:
        if resolved.startswith(prefix):
            return True
    return False


class PathSafety:
    """Path resolver that confines reads/writes to allowed roots + a deny-list.

    Args:
        roots: allowed roots (the run's ``base_folder_path`` + any ``writable``
            ``working_directories``). Realpath-normalized.
    """

    def __init__(self, roots: Sequence[str]) -> None:
        home = os.path.realpath(os.path.expanduser("~"))
        self._roots: Set[str] = {
            os.path.realpath(os.path.expanduser(r)) for r in roots if r
        }
        self._denied_paths = build_denied_paths(home)
        self._denied_prefixes = build_denied_prefixes(home)

    def resolve(self, path: str, *, allow_write: bool = False) -> Optional[str]:
        """Resolve *path* against the allowed roots.

        Returns the realpath if the target is inside an allowed root and not on
        the deny-list, else ``None`` (the caller turns None into an OWASP
        A01/A03 rejection). ``allow_write`` is reserved for ``WriteFileTool`` to
        additionally reject the deny-list strictly (writes never touch `.env`).
        """
        if not path:
            return None
        resolved = os.path.realpath(os.path.expanduser(str(path)))
        if is_path_denied(resolved, self._denied_paths, self._denied_prefixes):
            return None
        if allow_write:
            # Writes must be inside a root AND never touch app-owned state.
            for root in self._roots:
                if resolved == root or resolved.startswith(root + os.sep):
                    return resolved
            return None
        # Reads may also reach into any allowed root only.
        for root in self._roots:
            if resolved == root or resolved.startswith(root + os.sep):
                return resolved
        return None


def get_safe_roots_from_env(env_name: str = "WRITE_SAFE_ROOT") -> Set[str]:
    """Parse a ``os.pathsep``-separated env var into resolved safe roots."""
    env = os.getenv(env_name, "")
    if not env:
        return set()
    roots: Set[str] = set()
    for path in env.split(os.pathsep):
        if path:
            try:
                roots.add(os.path.realpath(os.path.expanduser(path)))
            except (OSError, ValueError):
                continue
    return roots


def is_env_basename(name: str) -> bool:
    """Case-insensitive .env-basename check (shared with redact.py)."""
    return Path(name).name.lower() in _BLOCKED_PROJECT_ENV_BASENAMES
