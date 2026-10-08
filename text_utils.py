import html
import re


def sanitize_text(text: str) -> str:
    """Normalize AI output for predictable TXT/DOCX/PDF rendering."""
    if not isinstance(text, str):
        return ""
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def text_to_html(text: str) -> str:
    safe = html.escape(sanitize_text(text))
    safe = re.sub(r"^(.+)$", r"<p>\1</p>", safe, flags=re.MULTILINE)
    safe = safe.replace("<p></p>", "")
    return safe.replace("\n", "")


def terms_to_list(terms: str) -> list[str]:
    return [item.strip() for item in terms.split(";") if item.strip()]
