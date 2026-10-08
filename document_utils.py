import html
import re
from typing import List


def sanitize_text(text: str) -> str:
    """Normalize AI text while preserving useful punctuation and structure."""
    if not text:
        return ""
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u00a0": " ",
        "\u2022": "-",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_terms(terms: str) -> List[str]:
    return [part.strip() for part in terms.split(";") if part.strip()]


def html_escape(text: str) -> str:
    return html.escape(sanitize_text(text))
