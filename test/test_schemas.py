
from schemas import InvoiceExtraction
from pydantic import ValidationError
import pytest
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src"),
)


def valid_invoice():
    return {
        "invoice_number": "INV-001",
        "vendor_name": "ABC Company",
        "invoice_date": "2026-10-23",
        "line_items": [
            {
                "description": "Office supplies",
                "quantity": 2,
                "unit_price": 25.00,
                "line_total": 50.00,
            }
        ],
        "subtotal": 50.00,
        "tax_amount": 5.00,
        "total_amount": 55.00,
        "currency": "USD",
    }


def test_valid_invoice():
    invoice = InvoiceExtraction.model_validate(valid_invoice())
    assert invoice.invoice_number == "INV-001"


def test_quantity_must_be_positive():
    data = valid_invoice()
    data["line_items"][0]["quantity"] = 0

    with pytest.raises(ValidationError):
        InvoiceExtraction.model_validate(data)


def test_currency_must_be_supported():
    data = valid_invoice()
    data["currency"] = "CAD"

    with pytest.raises(ValidationError):
        InvoiceExtraction.model_validate(data)


def test_total_must_match_items_and_tax():
    data = valid_invoice()
    data["total_amount"] = 80.00

    with pytest.raises(ValidationError):
        InvoiceExtraction.model_validate(data)


def test_negative_tax_is_rejected():
    data = valid_invoice()
    data["tax_amount"] = -1.00

    with pytest.raises(ValidationError):
        InvoiceExtraction.model_validate(data)
