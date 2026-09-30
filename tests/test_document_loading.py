from pathlib import Path

import fitz
from docx import Document

from core.document_loader import extract_document_text


def test_pdf_extraction(tmp_path):
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "This PDF contains workshop information.")
    doc.save(str(pdf_path))
    doc.close()

    text, pages = extract_document_text(pdf_path)

    assert "workshop information" in text.lower()
    assert pages >= 1


def test_docx_extraction(tmp_path):
    docx_path = tmp_path / "sample.docx"
    document = Document()
    document.add_paragraph("This DOCX contains the college syllabus.")
    document.save(str(docx_path))

    text, pages = extract_document_text(docx_path)

    assert "college syllabus" in text.lower()
    assert pages >= 1
