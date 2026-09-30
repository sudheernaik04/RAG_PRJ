from __future__ import annotations

import re


CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
MULTI_SPACE = re.compile(r"[ \t]{2,}")
MULTI_NEWLINES = re.compile(r"\n{3,}")
BROKEN_LINE = re.compile(r"(?<!\n)\s*\n\s*(?=\S)")


def clean_text(raw_text: str) -> str:
    """Clean extracted text while keeping meaningful content and structure."""
    if raw_text is None:
        return ""

    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00a0", " ")
    text = CONTROL_CHARS.sub(" ", text)
    text = text.replace("\t", " ")
    text = text.replace("\f", " ")
    text = BROKEN_LINE.sub(" ", text)
    text = MULTI_SPACE.sub(" ", text)
    text = MULTI_NEWLINES.sub("\n\n", text)
    text = text.strip()
    return text
