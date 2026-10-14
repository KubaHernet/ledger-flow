from datetime import date
from decimal import Decimal
from enum import StrEnum
from pydantic import BaseModel, Field
from uuid import UUID

class InvoiceStatus(StrEnum):
    OPEN = "open"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class CreateInvoiceRequest(BaseModel):
    invoice_number: str = Field(min_length=2, max_length=100, description="Unique identifier for the invoice")
    customer_id: str | None = None
    
    issue_date: date
    due_date: date
    amount: Decimal = Field(gt=0, description="Total amount for the invoice")
    currency: str = Field(min_length=3, max_length=3, description="Currency code in ISO 4217 format")
    
    status: InvoiceStatus = Field(default=InvoiceStatus.OPEN, description="Current status of the invoice")
    

class CreateInvoiceResponse(BaseModel):
    invoice_id: UUID