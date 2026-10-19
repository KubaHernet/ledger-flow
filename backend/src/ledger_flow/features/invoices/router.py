from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from ledger_flow.database import get_db
from ledger_flow.features.invoices.contracts import CreateInvoiceRequest, CreateInvoiceResponse, GetInvoiceResponse
from ledger_flow.features.invoices.create_invoice_handler import create_invoice as handle_create_invoice
from ledger_flow.features.invoices.get_invoice_handler import get_invoice as handle_get_invoice

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=CreateInvoiceResponse)
async def create_invoice(
    request: CreateInvoiceRequest,
    db: Annotated[Session, Depends(get_db)]
    ) -> CreateInvoiceResponse:
    return handle_create_invoice(request, db)

@router.get("/{invoice_id}", response_model=GetInvoiceResponse)
async def get_invoice(
    invoice_id: str,
    db: Annotated[Session, Depends(get_db),]
    ) -> GetInvoiceResponse:
    invoice = handle_get_invoice(invoice_id, db)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return invoice