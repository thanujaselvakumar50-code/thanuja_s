import html
import os
import re
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
ASSET_DIR = Path(__file__).resolve().parents[1] / "assets"
LOGO = ASSET_DIR / "logo.png"

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-title { text-align:center; font-size:42px; font-weight:800; margin-bottom:4px; }
    .subtitle { text-align:center; color:#8b93a7; margin-bottom:24px; }
    .preview {
        background:#111827; color:#f3f4f6; border-radius:14px; padding:24px;
        min-height:420px; max-height:650px; overflow-y:auto;
        border:1px solid #374151; white-space:pre-wrap;
        font-family: Georgia, serif; line-height:1.65;
    }
    .notice { padding:12px 16px; border-radius:10px; background:#fff7ed; border:1px solid #fed7aa; }
    </style>
    """,
    unsafe_allow_html=True,
)

if LOGO.exists():
    left, center, right = st.columns([1, 2, 1])
    with center:
        st.image(str(LOGO), width=130)

st.markdown('<div class="main-title">LegalEase</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-Powered Legal Document Generator</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Document Details")
    document_type = st.selectbox(
        "Document Type",
        [
            "Agreement",
            "Contract",
            "NDA (Non-Disclosure Agreement)",
            "Lease Agreement",
            "Employment Contract",
            "Employment Offer Letter",
            "Freelance Work Contract",
            "Other",
        ],
    )
    if document_type == "Other":
        document_type = st.text_input("Enter document type", placeholder="e.g. Service Agreement")

    parties = st.text_area(
        "Parties Involved",
        placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",
        height=120,
        help="Enter the names and roles of the people or organizations involved.",
    )
    terms = st.text_area(
        "Terms & Conditions",
        placeholder="Payment within 30 days; Confidentiality must be maintained; Either party may terminate with 15 days notice",
        height=180,
        help="Separate each clause with a semicolon (;).",
    )
    dates = st.text_input(
        "Effective Date",
        placeholder="April 10, 2025",
    )
    language = st.selectbox("Language", ["English", "Tamil", "Hindi", "Malayalam", "Telugu"])

    generate = st.button("Generate Document", type="primary", use_container_width=True)

if "document" not in st.session_state:
    st.session_state.document = ""
if "editing" not in st.session_state:
    st.session_state.editing = False

if generate:
    if not all([document_type, parties.strip(), terms.strip(), dates.strip()]):
        st.error("Please fill in Document Type, Parties Involved, Terms & Conditions, and Effective Date.")
    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates,
            "language": language,
        }
        try:
            with st.spinner("Generating your legal document..."):
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120,
                )
            if response.ok:
                data = response.json()
                st.session_state.document = data["document"]
                st.session_state.editing = False
                if data.get("mock_mode"):
                    st.warning("Demo mode is active. Set MOCK_MODE=false and add a Gemini API key for real AI generation.")
                else:
                    st.success("Document generated successfully.")
            else:
                try:
                    detail = response.json().get("detail", response.text)
                except Exception:
                    detail = response.text
                st.error(f"Backend error: {detail}")
        except requests.RequestException as exc:
            st.error(
                "Could not connect to the FastAPI backend. Start it first with: "
                "`python -m uvicorn backend.main:app --reload --port 8000`"
            )
            st.caption(str(exc))

st.subheader("Document Preview")

if st.session_state.document:
    if st.button("Click to Edit Document"):
        st.session_state.editing = not st.session_state.editing

    if st.session_state.editing:
        st.session_state.document = st.text_area(
            "Edit your document",
            value=st.session_state.document,
            height=600,
        )
        if st.button("Finish Editing"):
            st.session_state.editing = False
            st.rerun()
    else:
        safe = html.escape(st.session_state.document)
        st.markdown(f'<div class="preview">{safe}</div>', unsafe_allow_html=True)

    from utils.formatters import format_txt, format_docx, format_pdf

    txt_bytes = format_txt(st.session_state.document)
    docx_bytes = format_docx(st.session_state.document, document_type)
    pdf_bytes = format_pdf(st.session_state.document, document_type)

    st.subheader("Download / Save")
    c1, c2, c3 = st.columns(3)
    base_name = re.sub(r"[^A-Za-z0-9_-]+", "_", document_type.strip()).strip("_").lower() or "legal_document"
    with c1:
        st.download_button(
            "Download TXT",
            data=txt_bytes,
            file_name=f"{base_name}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with c2:
        st.download_button(
            "Download DOCX",
            data=docx_bytes,
            file_name=f"{base_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    with c3:
        st.download_button(
            "Download PDF",
            data=pdf_bytes,
            file_name=f"{base_name}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
else:
    st.info("Enter the document details in the sidebar and click Generate Document.")
    st.markdown(
        '<div class="notice"><b>Tip:</b> For Terms & Conditions, separate each clause with a semicolon (;), as specified in the project documentation.</div>',
        unsafe_allow_html=True,
    )

st.divider()
st.caption("LegalEase is a drafting aid. Review generated content with a qualified legal professional before real-world use.")
