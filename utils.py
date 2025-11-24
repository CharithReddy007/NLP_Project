# utils.py
import io
from typing import Union

# install PyPDF2 if you don't have it: pip install PyPDF2
from PyPDF2 import PdfReader

def extract_pdf(file_bytes: bytes) -> str:
    """
    Accepts raw bytes (from UploadFile.read()) and returns extracted text.
    """
    # wrap bytes into a file-like object
    fileobj = io.BytesIO(file_bytes)
    reader = PdfReader(fileobj)
    texts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            texts.append(text)
    return "\n".join(texts)


def extract_txt(file_bytes: bytes, encoding="utf-8") -> str:
    """
    Accept raw bytes and decode to string.
    """
    return file_bytes.decode(encoding, errors="replace")
