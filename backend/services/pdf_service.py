from io import StringIO
from pdfminer.high_level import extract_text
import logging

def extract_text_from_pdf(path):
    try:
        text = extract_text(path)
        return text or ''
    except Exception as e:
        logging.exception("PDF extraction failed")
        raise
