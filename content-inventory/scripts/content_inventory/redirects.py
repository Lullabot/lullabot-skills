"""Redirect resolution — CSV-based and optional HTTP chain following."""

import sys
import time

from .normalize import normalize_url


def resolve_redirects_from_csv(df):
    """Use the Redirect URL column from Screaming Frog data to resolve redirects.

    Returns a dict mapping normalized source URLs to their redirect target (full URL).
    Only includes rows that actually have a redirect.
    """
    redirects = {}
    for _, row in df.iterrows():
        redirect_url = row.get("Redirect URL", "")
        status_code = row.get("Status Code", "")
        if redirect_url and str(redirect_url).strip() and str(status_code) in ("301", "302"):
            source = row["normalized_url"]
            redirects[source] = str(redirect_url).strip()
    return redirects


def resolve_redirects_via_http(urls, delay=0.2, max_hops=10):
    """Follow HTTP redirect chains for a list of URLs.

    Returns a dict mapping original URL to final destination URL.
    Mirrors the getFinalUrl Google Apps Script behavior — every URL
    gets a result, even if it doesn't redirect (returns itself).
    """
    try:
        import requests
    except ImportError:
        print("Warning: 'requests' package not installed. Skipping HTTP redirect resolution.", file=sys.stderr)
        return {}

    results = {}
    for url in urls:
        full_url = url if url.startswith("http") else f"https://{url}"
        current = full_url
        try:
            for _ in range(max_hops):
                resp = requests.head(current, allow_redirects=False, timeout=10)
                if resp.status_code in (301, 302):
                    location = resp.headers.get("Location", "")
                    if not location:
                        results[url] = "Redirect with no Location header"
                        break
                    if location.startswith("/"):
                        from urllib.parse import urlparse
                        parsed = urlparse(current)
                        location = f"{parsed.scheme}://{parsed.netloc}{location}"
                    current = location
                else:
                    results[url] = current
                    break
            else:
                results[url] = "Too many redirects"
        except Exception as e:
            results[url] = f"Error: {e}"
        time.sleep(delay)
    return results
