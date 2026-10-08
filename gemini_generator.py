import os
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
except ImportError:  # pragma: no cover
    genai = None


class GeminiDocumentGenerator:
    """Gemini-backed legal document generator.

    The original project document names Gemini 1.5 Pro. The current implementation
    reads GEMINI_MODEL from .env so the model can be updated without changing code.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
        self.mock_mode = os.getenv("MOCK_MODE", "false").lower() == "true"
        self.client = None

        if not self.mock_mode and self.api_key:
            if genai is None:
                raise RuntimeError(
                    "google-genai is not installed. Run: pip install -r requirements.txt"
                )
            self.client = genai.Client(api_key=self.api_key)

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
        language: str = "English",
    ) -> str:
        if self.mock_mode:
            return self._mock_document(document_type, parties, terms, dates, language)

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Add it to the .env file, or set MOCK_MODE=true for local testing."
            )

        prompt = f"""
You are the LegalEase legal-document drafting engine.

Create a professional, structured draft for the requested legal document.

Document type:
{document_type}

Parties involved:
{parties}

Terms and conditions:
{terms}

Effective date:
{dates}

Output language:
{language}

Requirements:
- Produce only the document draft, not a discussion about how you created it.
- Use a clear title and professional section headings.
- Include the named parties and effective date accurately.
- Convert the supplied terms into suitable clauses without inventing important facts.
- Include reasonable standard clauses only when they are appropriate to the document type.
- Include signature blocks at the end.
- Do not claim that the document is guaranteed legally valid.
- Do not invent names, addresses, monetary amounts, laws, courts, registration numbers, or jurisdiction-specific requirements that were not supplied.
- If an important fact is missing, use a neutral placeholder such as [TO BE COMPLETED].
- Keep the output editable as plain text.
"""

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            text = getattr(response, "text", None)
            if not text:
                raise RuntimeError("Gemini returned an empty response.")
            return text.strip()
        except Exception as exc:
            raise RuntimeError(f"Gemini generation failed: {exc}") from exc

    @staticmethod
    def _mock_document(document_type, parties, terms, dates, language):
        clauses = [item.strip() for item in terms.split(";") if item.strip()]
        term_lines = "\n".join(
            f"{idx}. {clause}" for idx, clause in enumerate(clauses, start=1)
        )
        return f"""LEGAL DOCUMENT DRAFT

{document_type.upper()}

Effective Date: {dates}

PARTIES
{parties}

1. PURPOSE
This document records the understanding between the parties identified above.

2. TERMS AND CONDITIONS
{term_lines}

3. GENERAL PROVISIONS
The parties agree to act in good faith and comply with the terms recorded in this document.

4. SIGNATURES

Party 1: ______________________________
Name: _________________________________
Date: __________________________________

Party 2: ______________________________
Name: _________________________________
Date: __________________________________

[DEMO MODE: This draft was generated locally because MOCK_MODE=true.]
"""
