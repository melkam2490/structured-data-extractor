import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from schemas import InvoiceExtraction

from pydantic import ValidationError
import pytest



def valid_invoice():
    return {
        "vendor_name": "ABC Store",
        "invoice_number": "INV-001",
        "invoice_date": "2026-10-23",
        "currency": "USD",
        "line_items": [
            {
                "description": "Laptop",
                "quantity": 2,
                "unit_price": 100,
                "line_total": 200,
            }
        ],
        "subtotal": 200,
        "tax_amount": 20,
        "total_amount": 220,
    }


def test_valid_invoice():
    invoice = InvoiceExtraction(**valid_invoice())
    assert invoice.total_amount == 220


def test_quantity_must_be_positive():
    data = valid_invoice()
    data["line_items"][0]["quantity"] = 0

    with pytest.raises(ValidationError):
        InvoiceExtraction(**data)


def test_currency_must_be_supported():
    data = valid_invoice()
    data["currency"] = "CAD"

    with pytest.raises(ValidationError):
        InvoiceExtraction(**data)


def test_total_must_match_items_and_tax():
    data = valid_invoice()
    data["total_amount"] = 250

    with pytest.raises(ValidationError):
        InvoiceExtraction(**data)


def test_negative_tax_is_rejected():
    data = valid_invoice()
    data["tax_amount"] = -5

    with pytest.raises(ValidationError):
        InvoiceExtraction(**data)
