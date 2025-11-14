import pytesseract
from PIL import Image
import logging

def extract_text_from_image(path):
    try:
        img = Image.open(path)
        text = pytesseract.image_to_string(img, lang='eng')
        return text or ''
    except Exception as e:
        logging.exception("OCR failed")
        raise
