from PyPDF2 import PdfReader
import logging

logging.basicConfig(level=logging.INFO)

def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        if reader.is_encrypted:
            reader.decrypt("")
        text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
        return text.strip() if text else "Error: No readable text found in PDF."
    except Exception as e:
        logging.error(f"Error reading PDF: {e}")
        return f"Error reading PDF: {e}"
