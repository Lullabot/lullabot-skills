"""URL normalization for content inventory processing."""

import re


def normalize_url(url: str) -> str:
    """Normalize a URL by stripping protocol, www, query params, fragments,
    trailing slashes, and whitespace. Returns lowercase.

    Idempotent: works on both full URLs and already-partially-normalized URLs.
    """
    if not url or not isinstance(url, str):
        return ""
    # Strip leading/trailing whitespace first
    result = url.strip()
    # Strip protocol and www
    result = re.sub(r"^https?://(www\.)?", "", result)
    # Strip query params and fragments
    result = re.sub(r"[?#].*$", "", result)
    # Strip trailing slashes
    result = re.sub(r"/+$", "", result)
    # Strip whitespace
    result = re.sub(r"\s+", "", result)
    return result.lower()
