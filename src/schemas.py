
from pydantic import BaseModel, Field, model_validator
from typing import Literal


class LineItem(BaseModel):
    description: str
    quantity: float = Field(gt=0)
    unit_price: float = Field(ge=0)
    line_total: float = Field(ge=0)


class InvoiceExtraction(BaseModel):
    vendor_name: str
    invoice_number: str
    invoice_date: str
    currency: Literal["USD", "EUR", "GBP"]
    line_items: list[LineItem]
    subtotal: float = Field(ge=0)
    tax_amount: float = Field(ge=0)
    total_amount: float = Field(ge=0)

    @model_validator(mode="after")
    def check_invoice_totals(self):
        calculated_subtotal = sum(
            item.line_total for item in self.line_items
        )

        if abs(calculated_subtotal - self.subtotal) > 0.02:
            raise ValueError(
                "Subtotal must match the sum of line item totals"
            )

        expected_total = self.subtotal + self.tax_amount

        if abs(expected_total - self.total_amount) > 0.02:
            raise ValueError(
                "Total must equal subtotal plus tax"
            )

        return self
