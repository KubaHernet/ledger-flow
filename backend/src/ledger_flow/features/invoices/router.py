from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from ledger_flow.database import get_db
from ledger_flow.features.invoices.contracts import CreateInvoiceRequest, CreateInvoiceResponse
from ledger_flow.features.invoices.create_invoice import create_invoice as create_invoice_service

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=CreateInvoiceResponse)
async def create_invoice(
    request: CreateInvoiceRequest,
    db: Annotated[Session, Depends(get_db)]
    ) -> CreateInvoiceResponse:
    return create_invoice_service(request, db)