import sys
from pathlib import Path

PROJECT_FOLDER = Path(__file__).resolve().parents[1]
SRC_FOLDER = PROJECT_FOLDER / "src"
sys.path.insert(0, str(SRC_FOLDER))

import fallback


def test_reflection_succeeds_on_second_attempt(monkeypatch):
    valid_data = {
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

    responses = [
        {"vendor_name": "ABC Store"},
        valid_data,
    ]

    def fake_extract_with_ai(raw_text, previous_error=None):
        return responses.pop(0)

    monkeypatch.setattr(
        fallback, "extract_with_ai", fake_extract_with_ai
    )

    result = fallback.extract_with_retry(
        "Test invoice", max_retries=2
    )

    assert result["attempts_used"] == 2
    assert result["status"] == "REPAIRED_VIA_REFLECTION"


def test_failed_extraction_goes_to_dead_letter_queue(
    monkeypatch, tmp_path
):
    monkeypatch.chdir(tmp_path)

    def fake_extract_with_ai(raw_text, previous_error=None):
        raise ValueError("Simulated extraction failure")

    monkeypatch.setattr(
        fallback, "extract_with_ai", fake_extract_with_ai
    )

    result = fallback.extract_with_retry(
        "Bad invoice", max_retries=2
    )

    assert result["status"] == "DLQ_FAILED"
    assert result["attempts_used"] == 2
    assert Path(
        "dead_letter_queue/failed_invoice.json"
    ).exists()
