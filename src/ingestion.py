
from io import BytesIO

from pypdf import PdfReader
from bs4 import BeautifulSoup


def extract_pdf_text(file_bytes):
    """Extract text from an uploaded PDF file."""
    pdf = PdfReader(BytesIO(file_bytes))
    text = ""

    for page in pdf.pages:
        text += (page.extract_text() or "") + "\n"

    return text.strip()


def extract_html_text(html):
    """Extract readable text from HTML invoice content."""
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)
