import streamlit as st
from pypdf import PdfReader

st.set_page_config(
    page_title="UniPilot AI",
    page_icon="🎓"
)

st.title("🎓 UniPilot AI")
st.write("AI-powered university document assistant.")

st.subheader("📄 Upload a university document")

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"]
)

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    st.success("Document uploaded successfully!")

    st.subheader("📖 Document Preview")

    if text.strip():
        st.text_area(
            "Extracted text",
            text,
            height=400
        )
    else:
        st.warning("No readable text was found in this PDF.")