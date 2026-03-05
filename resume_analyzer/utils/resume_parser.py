import pdfplumber

def extract_text_from_resume(uploaded_file):
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text = text + page_text + "\n"
    except Exception as e:
        raise RuntimeError(f"Error reading the PDF: {e}")
    return text.strip()