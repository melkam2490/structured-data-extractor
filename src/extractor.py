
from pydantic import ValidationError

from schemas import InvoiceExtraction


def validate_invoice(data: dict) -> InvoiceExtraction:
    """
    Check invoice data against our Pydantic schema.
    """
    try:
        invoice = InvoiceExtraction.model_validate(data)
        return invoice

    except ValidationError as error:
        print("Invoice validation failed:")
        print(error)
        raise
