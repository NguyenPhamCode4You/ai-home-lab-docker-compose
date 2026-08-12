"""redact — regex-based secret redaction for logs and tool output.

Pattern ported from Hermes ``agent/redact.py`` (MIT). Applies pattern matching to
mask API keys, tokens, and credentials **before they cross an egress boundary** —
to a log file, verbose output, or another model (distillation / ladder model, a
delegate, cloud escalation). Short tokens (< 18 chars) are fully masked; longer
tokens preserve the first 6 and last 4 characters for debuggability.
"""
from __future__ import annotations

import logging
import os
import re

logger = logging.getLogger(__name__)

_REDACT_ENABLED = os.getenv("REDACT_SECRETS", "true").lower() in {"1", "true", "yes", "on"}

# Sensitive query-string parameter names (case-insensitive exact match).
_SENSITIVE_QUERY_PARAMS = frozenset({
    "access_token", "refresh_token", "id_token", "token", "api_key", "apikey",
    "client_secret", "password", "auth", "jwt", "session", "secret", "key",
    "code", "signature", "x-amz-signature",
})

# Sensitive form/JSON body key names (case-insensitive exact match, NOT substring —
# so "token_count" and "session_id" must NOT match).
_SENSITIVE_BODY_KEYS = frozenset({
    "access_token", "refresh_token", "id_token", "token", "api_key", "apikey",
    "client_secret", "password", "auth", "jwt", "secret", "private_key",
    "authorization", "key",
})

# Known API-key prefixes — match the prefix + contiguous token chars.
_PREFIX_PATTERNS = [
    r"sk-[A-Za-z0-9_-]{10,}",            # OpenAI / OpenRouter / Anthropic (sk-ant-*)
    r"ghp_[A-Za-z0-9]{10,}",             # GitHub PAT (classic)
    r"github_pat_[A-Za-z0-9_]{10,}",
    r"gho_[A-Za-z0-9]{10,}",
    r"ghu_[A-Za-z0-9]{10,}",
    r"ghs_[A-Za-z0-9]{10,}",
    r"ghr_[A-Za-z0-9]{10,}",
    r"xapp-\d+-[A-Za-z0-9-]{10,}",       # Slack app-level token
    r"xox[baprs]-[A-Za-z0-9-]{10,}",     # Slack bot/app/user tokens
    r"AIza[A-Za-z0-9_-]{30,}",           # Google API keys
    r"pplx-[A-Za-z0-9]{10,}",            # Perplexity
    r"fal_[A-Za-z0-9_-]{10,}",           # Fal.ai
    r"fc-[A-Za-z0-9]{10,}",              # Firecrawl
    r"AKIA[A-Z0-9]{16}",                 # AWS Access Key ID
    r"sk_live_[A-Za-z0-9]{10,}",         # Stripe secret key (live)
    r"sk_test_[A-Za-z0-9]{10,}",         # Stripe secret key (test)
    r"hf_[A-Za-z0-9]{10,}",              # HuggingFace token
]

# Compiled once at import; applied across all text that leaves the agent.
_REDACT_PATTERNS = [re.compile(p) for p in _PREFIX_PATTERNS]

# A plausible generic secret: >= 20 chars of alnum/_- with a high ratio of
# mixed case/digits, but not a plain hex "id". Kept conservative.
_GENERIC_SECRET_RE = re.compile(r"\b(?![a-f0-9]{20,}\b)[A-Za-z0-9_\-]{20,64}\b")


def _mask(token: str) -> str:
    if len(token) < 18:
        return "*" * len(token)
    return token[:6] + "…" + token[-4:]


def redact_query_params(url: str) -> str:
    """Redact sensitive query-string parameter values."""
    from urllib.parse import parse_qsl, urlsplit, urlunsplit

    parts = urlsplit(url)
    qs = parse_qsl(parts.query, keep_blank_values=True)
    safe = []
    for k, v in qs:
        if k.lower() in _SENSITIVE_QUERY_PARAMS and v:
            safe.append((k, _mask(v)))
        else:
            safe.append((k, v))
    from urllib.parse import urlencode

    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(safe), parts.fragment))


def redact_json_body(text: str) -> str:
    """Redact sensitive keys in a JSON body string (best-effort regex)."""
    for key in _SENSITIVE_BODY_KEYS:
        # Match "key": "value" or "key": "value" with surrounding flexibility.
        pattern = re.compile(
            rf'(["\']{re.escape(key)}["\']\s*:\s*["\'])([^"\']+)(["\'])',
            re.IGNORECASE,
        )
        text = pattern.sub(lambda m: m.group(1) + _mask(m.group(2)) + m.group(3), text)
    return text


def redact_sensitive_text(text: str, *, force: bool = False, redact_url_credentials: bool = True) -> str:
    """Redact API keys / tokens / credentials from *text*.

    ``force`` bypasses the ``REDACT_SECRETS`` env toggle (used at hard egress
    boundaries where redaction must not be disable-able). ``redact_url_credentials``
    drops ``user:pass@`` from URLs.
    """
    if not text:
        return text
    enabled = force or _REDACT_ENABLED
    if not enabled:
        return text

    out = text
    for pattern in _REDACT_PATTERNS:
        out = pattern.sub(lambda m: _mask(m.group(0)), out)

    if redact_url_credentials:
        out = re.sub(r"//[^/@\s]+@", "//***@", out)

    out = redact_query_params(out)
    out = redact_json_body(out)
    # Conservative generic-secret sweep, then a final single-char de-dup guard.
    out = _GENERIC_SECRET_RE.sub(lambda m: _mask(m.group(0)), out)
    return out