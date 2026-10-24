
import json
import os

from json_repair import repair_json
from pydantic import ValidationError

from schemas import InvoiceExtraction
from ai_extractor import extract_with_ai


def validate_with_fallback(data):
    try:
        invoice = InvoiceExtraction.model_validate(data)
        return {
            "status": "SUCCESS",
            "invoice": invoice.model_dump(mode="json"),
            "error": None,
        }
    except ValidationError as error:
        return {
            "status": "VALIDATION_FAILED",
            "invoice": None,
            "error": str(error),
        }


def extract_with_retry(raw_text, max_retries=3):
    error_log = []
    previous_error = None

    for attempt in range(1, max_retries + 1):
        try:
            data = extract_with_ai(
                raw_text,
                previous_error=previous_error,
            )
            invoice = InvoiceExtraction.model_validate(data)

            return {
                "status": (
                    "SUCCESS" if attempt == 1
                    else "REPAIRED_VIA_REFLECTION"
                ),
                "validated_data": invoice.model_dump(mode="json"),
                "attempts_used": attempt,
                "error_log": error_log,
            }

        except Exception as error:
            previous_error = str(error)
            error_log.append(previous_error)

    # Try to repair JSON if the original text contains JSON.
    try:
        repaired = repair_json(raw_text, return_objects=True)
        invoice = InvoiceExtraction.model_validate(repaired)

        return {
            "status": "REPAIRED_VIA_REFLECTION",
            "validated_data": invoice.model_dump(mode="json"),
            "attempts_used": max_retries,
            "error_log": error_log,
        }

    except Exception as error:
        error_log.append(str(error))

    # Save failed records for later review.
    os.makedirs("dead_letter_queue", exist_ok=True)
    with open(
        "dead_letter_queue/failed_invoice.json",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            {"raw_text": raw_text, "error_log": error_log},
            file,
            indent=2,
        )

    return {
        "status": "DLQ_FAILED",
        "validated_data": None,
        "attempts_used": max_retries,
        "error_log": error_log,
    }
