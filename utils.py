from pypdf import PdfReader

def extract_text_from_pdf(pdf_file):
    """Extracts all text from an uploaded PDF file."""
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    return text