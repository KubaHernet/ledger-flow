from datetime import date
from decimal import Decimal

from ledger_flow.features.invoices.contracts import InvoiceStatus
from pydantic import BaseModel, Field


class ImportInvoicesResponse(BaseModel):
    imported_count: int
    
    
class ImportInvoiceRow(BaseModel):
    invoice_number: str = Field(min_length=1, max_length=100)
    customer_name: str = Field(min_length=1, max_length=200)
    customer_id: str | None = None

    issue_date: date
    due_date: date

    amount: Decimal = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)

    status: InvoiceStatus | None = Field(default=None, description="Current status of the invoice")