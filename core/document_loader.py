from __future__ import annotations

from pathlib import Path
from typing import Tuple

import fitz
from docx import Document


def extract_pdf_text(file_path: str | Path) -> tuple[str, int]:
    """Extract text from a PDF and preserve page boundaries."""
    path = Path(file_path)
    doc = fitz.open(str(path))
    page_count = doc.page_count
    page_texts = []
    parts = []

    for page_number in range(page_count):
        page = doc.load_page(page_number)
        text = page.get_text("text").strip()
        page_texts.append(text)
        if text:
            parts.append(f"[Page {page_number + 1}] {text}")

    doc.close()
    full_text = "\n\n".join(parts)
    return full_text, page_count


def extract_docx_text(file_path: str | Path) -> tuple[str, int]:
    """Extract text from a DOCX file."""
    path = Path(file_path)
    doc = Document(str(path))
    paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return "\n\n".join(paragraphs), max(1, len(paragraphs))


def extract_document_text(file_path: str | Path) -> tuple[str, int]:
    """Extract text from a PDF or DOCX file."""
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return extract_pdf_text(path)
    if suffix == ".docx":
        return extract_docx_text(path)

    raise ValueError(f"Unsupported file type: {suffix}. Please upload a PDF or DOCX file.")
