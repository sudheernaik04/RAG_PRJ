from __future__ import annotations

import re
from typing import Any

from core.text_cleaner import clean_text


def _infer_page_number(raw_text: str, char_offset: int) -> int | None:
    matches = list(re.finditer(r"\[Page\s+(\d+)\]", raw_text, flags=re.IGNORECASE))
    if not matches:
        return None

    page_number = None
    for match in matches:
        if match.start() <= char_offset:
            page_number = int(match.group(1))
    return page_number


def chunk_text(
    text: str,
    chunk_size: int = 400,
    overlap: int = 80,
    source_name: str = "document",
) -> list[dict[str, Any]]:
    """Split text into overlapping chunks while attaching metadata."""
    cleaned = clean_text(text)
    if not cleaned:
        return []

    chunk_size = max(10, int(chunk_size))
    overlap = max(0, min(int(overlap), chunk_size - 1))
    step = max(1, chunk_size - overlap)

    words = cleaned.split()
    if len(words) <= chunk_size:
        word_groups = [words]
    else:
        word_groups = [words[i : i + chunk_size] for i in range(0, len(words), step)]

    chunks = []
    char_cursor = 0
    for index, word_group in enumerate(word_groups):
        chunk_text_value = " ".join(word_group).strip()
        if not chunk_text_value:
            continue

        page_number = _infer_page_number(cleaned, char_cursor)
        chunks.append(
            {
                "chunk_id": f"{source_name}_{index + 1}",
                "text": chunk_text_value,
                "source_name": source_name,
                "page_number": page_number,
                "chunk_index": index + 1,
                "start_char": char_cursor,
            }
        )
        char_cursor += len(chunk_text_value) + 1

    return chunks
