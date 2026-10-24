
import streamlit as st

from ingestion import extract_pdf_text, extract_html_text
from fallback import extract_with_retry

st.title("Invoice Data Extractor")
st.write("Upload a PDF or paste invoice HTML.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
html_input = st.text_area("Paste HTML invoice")

if st.button("Extract and Validate"):
    raw_text = ""

    try:
        if uploaded_file:
            raw_text = extract_pdf_text(uploaded_file.getvalue())
        elif html_input.strip():
            raw_text = extract_html_text(html_input)
        else:
            st.warning("Upload a PDF or paste HTML.")
            st.stop()

        st.subheader("Original Invoice Text")
        st.text_area("Extracted text", raw_text, height=180)

        with st.spinner("Extracting and validating invoice..."):
            result = extract_with_retry(raw_text)

        st.subheader("Extraction Result")
        st.write("Status:", result["status"])
        st.write("Attempts:", result["attempts_used"])
        st.json(result["validated_data"] or {})

        if result["error_log"]:
            st.subheader("Error Log")
            st.write(result["error_log"])

    except Exception as error:
        st.error(f"Something went wrong: {error}")
