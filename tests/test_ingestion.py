
from ingestion import extract_html_text, extract_pdf_text
import sys
from pathlib import Path
from io import BytesIO

from pypdf import PdfWriter

PROJECT_FOLDER = Path(__file__).resolve().parents[1]
SRC_FOLDER = PROJECT_FOLDER / "src"
sys.path.insert(0, str(SRC_FOLDER))


def test_extract_html_text():
    html = """
    <html>
        <body>
            <h1>ABC Store</h1>
            <p>Invoice Number: INV-001</p>
        </body>
    </html>
    """

    result = extract_html_text(html)

    assert "ABC Store" in result
    assert "INV-001" in result


def test_extract_pdf_text():
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)

    pdf_bytes = BytesIO()
    writer.write(pdf_bytes)

    result = extract_pdf_text(pdf_bytes.getvalue())

    assert isinstance(result, str)
