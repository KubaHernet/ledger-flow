from fastapi import APIRouter, status
from uuid import uuid4
from ledger_flow.features.invoices.contracts import CreateInvoiceRequest, CreateInvoiceResponse

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=CreateInvoiceResponse)
async def create_invoice(request: CreateInvoiceRequest):
    response = CreateInvoiceResponse(invoice_id=uuid4())
    return response