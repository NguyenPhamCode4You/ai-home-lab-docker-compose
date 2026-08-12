"""bounded_io — byte-capped, deadline-bounded reads for every external call.

Pattern ported from Hermes ``agent/bounded_response.py`` (MIT). The key insight:
a wall-clock check *between* yielded chunks cannot interrupt a socket read that
stalls mid-chunk (control never returns to Python until the client's own read
timeout fires). So the read runs on a **daemon worker thread** and the caller
waits on it with a hard deadline; on timeout we close the response (which
unblocks / cancels the read) and return whatever partial bytes arrived.

Used by the ``models_ladder`` clients (Ollama / OpenRouter) and by the tools to
guarantee a stalled local endpoint never hangs the run. A deadline hit counts as
one **infra failure** against ``max_retries_until_switching_models`` (§4).
"""
from __future__ import annotations

import logging
import threading
from typing import List, Optional

import httpx

logger = logging.getLogger(__name__)

DEFAULT_MAX_BYTES = 64 * 1024
DEFAULT_TIMEOUT_S = 10.0


def _safe_close(response: httpx.Response) -> None:
    try:
        response.close()
    except Exception:  # noqa: BLE001 - best-effort on the error path
        pass


def read_bounded(
    response: httpx.Response,
    *,
    max_bytes: int = DEFAULT_MAX_BYTES,
    timeout_s: float = DEFAULT_TIMEOUT_S,
) -> str:
    """Read a response body with a byte cap and a hard wall-clock deadline.

    Returns the decoded text (UTF-8, errors replaced), truncated to ``max_bytes``.
    Never raises: any transport error, stall, or oversize condition is swallowed
    and the best-effort partial text (or an empty string) is returned — callers
    use this on the error path and must not mask the original failure.

    The byte cap protects against huge bodies; the wall-clock deadline (enforced
    via a worker thread so it can interrupt a socket read that stalls mid-chunk)
    protects against bodies that open and then hang.
    """
    chunks: List[bytes] = []
    state = {"truncated": False}
    done = threading.Event()

    def _drain() -> None:
        total = 0
        try:
            for chunk in response.iter_bytes():
                if not chunk:
                    continue
                remaining = max_bytes - total
                if remaining <= 0:
                    state["truncated"] = True
                    break
                if len(chunk) > remaining:
                    chunks.append(chunk[:remaining])
                    total += remaining
                    state["truncated"] = True
                    break
                chunks.append(chunk)
                total += len(chunk)
        except Exception as exc:  # noqa: BLE001 - error path must not raise
            logger.debug("bounded read failed: %s", exc)
        finally:
            done.set()

    worker = threading.Thread(target=_drain, name="bounded-io-read", daemon=True)
    worker.start()
    finished = done.wait(timeout=timeout_s)

    if not finished:
        logger.debug(
            "bounded read: hard timeout after %.1fs (%d bytes so far)",
            timeout_s,
            sum(len(c) for c in chunks),
        )
        # Closing the response cancels the in-flight socket read, letting the
        # worker thread unwind. We do not join (it is a daemon and may be
        # blocked in C); the partial `chunks` collected so far are returned.
        _safe_close(response)
    else:
        _safe_close(response)

    if state["truncated"]:
        logger.debug(
            "bounded read: capped at %d bytes (max=%d)",
            sum(len(c) for c in chunks),
            max_bytes,
        )
    return b"".join(chunks).decode("utf-8", errors="replace")


def read_bounded_or_default(
    response: httpx.Response,
    *,
    max_bytes: int = DEFAULT_MAX_BYTES,
    timeout_s: float = DEFAULT_TIMEOUT_S,
) -> Optional[str]:
    """Like ``read_bounded`` but returns ``None`` on an empty body.

    Convenience for callers that distinguish "no body" from "empty string".
    """
    text = read_bounded(response, max_bytes=max_bytes, timeout_s=timeout_s)
    return text or None
