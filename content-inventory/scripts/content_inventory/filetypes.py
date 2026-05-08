"""Extension-based file type classification."""

import re

EXTENSION_MAP = {
    "pdf": "PDF",
    "png": "Image",
    "jpg": "Image",
    "jpeg": "Image",
    "jfif": "Image",
    "svg": "Image",
    "gif": "GIF",
    "docx": "Word document",
    "doc": "Word document",
    "xlsx": "Spreadsheet",
    "xls": "Spreadsheet",
    "xlsm": "XLSM",
    "pptx": "PPT",
    "ppt": "PPT",
    "mp4": "Video",
    "avi": "Video",
    "mov": "Video",
    "wmv": "Video",
    "zip": "Archive",
    "csv": "CSV",
    "txt": "Text",
}


def classify_file_type(url: str) -> str:
    """Classify a file by its URL extension.

    Handles uppercase extensions, percent-encoded URLs, and query params
    that appear after the extension.
    """
    if not url or not isinstance(url, str):
        return "Unknown"
    # Strip query params and fragments first
    clean = re.sub(r"[?#].*$", "", url)
    # Extract extension from the last path segment
    match = re.search(r"\.([a-zA-Z0-9]+)$", clean)
    if not match:
        return "Unknown"
    ext = match.group(1).lower()
    return EXTENSION_MAP.get(ext, ext.upper())
