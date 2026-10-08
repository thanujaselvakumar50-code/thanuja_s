from services.document_service import format_docx, format_pdf
from utils.text_utils import sanitize_text, terms_to_list


def test_sanitize_text():
    assert sanitize_text("Hello\u2014world\n\n\nNext") == "Hello-world\n\nNext"


def test_terms_to_list():
    assert terms_to_list("A; B; ; C") == ["A", "B", "C"]


def test_docx_export():
    data = format_docx("INTRODUCTION\nThis is a draft.", "NDA", "Confidentiality; Term of 1 year")
    assert data[:2] == b"PK"


def test_pdf_export():
    data = format_pdf("INTRODUCTION\nThis is a draft.", "NDA")
    assert data.startswith(b"%PDF")
