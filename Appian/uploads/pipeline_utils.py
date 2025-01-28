import logging
from ocr import extract_text_from_pdf
from nlp import summarize_text, classify_document, extract_entities

logging.basicConfig(level=logging.INFO)

def process_document(pdf_path):
    logging.info(f"Processing document: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    if "Error" in text:
        return {"error": text}

    doc_type, confidence = classify_document(text)
    summary = summarize_text(text)
    entities = extract_entities(text)

    return {
        'document_type': doc_type,
        'confidence': round(confidence, 2),
        'summary': summary,
        'extracted_data': entities,
        'raw_text': text,
    }
