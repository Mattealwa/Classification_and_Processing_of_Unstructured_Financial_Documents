import re
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO)

# Initialize Hugging Face pipelines
try:
    summarizer = pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-6-6",
        cache_dir="./models/summarization"
    )
    classifier = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        cache_dir="./models/classification"
    )
    logging.info("NLP pipelines initialized successfully.")
except Exception as e:
    logging.error(f"Error initializing NLP pipelines: {e}")
    summarizer = None
    classifier = None

def summarize_text(text):
    if summarizer is None:
        logging.error("Summarization pipeline is not available.")
        return "Summarization pipeline is not available."
    try:
        summary = summarizer(text[:512], max_length=150, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        logging.error(f"Error summarizing text: {e}")
        return "Error generating summary."

def classify_document(text):
    if classifier is None:
        logging.error("Classification pipeline is not available.")
        return "unknown", 0
    try:
        labels = ['application', 'identity', 'financial', 'receipt', 'invoice', 'tax']
        result = classifier(text, labels)
        return result['labels'][0], result['scores'][0]
    except Exception as e:
        logging.error(f"Error classifying document: {e}")
        return "unknown", 0

def extract_entities(text):
    try:
        entities = {
            "names": re.findall(r'\b[A-Z][a-z]*\s[A-Z][a-z]*\b', text),
            "dates": re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b', text),
            "amounts": re.findall(r'\$\s?\d+(?:,\d{3})*(?:\.\d+)?', text),
            "addresses": re.findall(r'\d{1,5}\s\w+(\s\w+)*,\s\w+,\s\w+', text),
        }
        return entities
    except Exception as e:
        logging.error(f"Error extracting entities: {e}")
        return {}
