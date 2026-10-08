# LegalEase — AI-Powered Legal Document Generator

LegalEase follows the supplied project documentation: Streamlit frontend, FastAPI backend, Gemini AI generation, editable preview, and TXT/DOCX/PDF export.

## Project structure

```text
LegalEase/
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── routes.py
├── frontend/
│   └── app.py
├── utils/
│   ├── __init__.py
│   ├── document_utils.py
│   └── formatters.py
├── assets/
│   └── logo.png
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── Dockerfile
├── Procfile
├── requirements.txt
└── README.md
```

## 1. VS Code setup

Open this folder in VS Code. In the VS Code terminal:

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, you can run without activation:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Then select the interpreter:
`Ctrl+Shift+P` → `Python: Select Interpreter` → choose `.venv\Scripts\python.exe`.

## 2. Configure Gemini

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Open `.env` and put your Gemini API key in `GEMINI_API_KEY`.

The project uses the current `google-genai` Python SDK. The supplied document mentions Gemini 1.5 Pro, but that older model should not be hard-coded for a new 2026 project. The default here is `gemini-3.8-flash`; you can change `GEMINI_MODEL` if your account supports another current model.

## 3. Start the backend

From the project root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Open:
http://127.0.0.1:8000
and API docs:
http://127.0.0.1:8000/docs

## 4. Start the Streamlit frontend

Open a second terminal in the same project folder:

```powershell
.\.venv\Scripts\python.exe -m streamlit run frontend/app.py
```

Streamlit normally opens:
http://localhost:8501

## 5. Test without a Gemini key

For UI/backend testing only, set:

```env
MOCK_MODE=true
```

The app will generate a clearly labelled demo document locally. Set it back to `false` for real Gemini generation.

## 6. Test the backend

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## 7. What to test

1. Choose a document type.
2. Enter parties involved.
3. Enter semicolon-separated terms.
4. Enter an effective date.
5. Click Generate Document.
6. Review the styled preview.
7. Click Edit Document and change text.
8. Download TXT, DOCX, and PDF.
9. Open the downloaded files and verify the LegalEase branding/footer.

## Important legal note

LegalEase is a document drafting aid, not a substitute for a qualified lawyer. Generated text should be reviewed before being used for a real legal matter.
