from typing import Annotated
from ledger_flow.features.invoices.invoices_import.contracts import ImportInvoicesResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from ledger_flow.database import get_db
from ledger_flow.features.invoices.contracts import CreateInvoiceRequest, CreateInvoiceResponse, GetInvoiceListResponse, GetInvoiceResponse, UpdateInvoiceRequest, UpdateInvoiceResponse
from ledger_flow.features.invoices.create_invoice_handler import create_invoice as handle_create_invoice
from ledger_flow.features.invoices.get_invoice_handler import get_invoice as handle_get_invoice
from ledger_flow.features.invoices.get_invoices_handler import get_invoices as handle_get_invoices
from ledger_flow.features.invoices.update_incoice_handler import update_invoice as handle_update_invoice
from ledger_flow.features.invoices.invoices_import.import_invoices_handler import import_invoices as handle_import_invoices

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post(
    "/import",
    status_code=status.HTTP_201_CREATED,
    response_model=ImportInvoicesResponse
)
async def import_invoices_endpoint(
    file: UploadFile,
    db: Annotated[Session, Depends(get_db),]
):
    return handle_import_invoices(file, db)

@router.get("/{invoice_id}", response_model=GetInvoiceResponse)
async def get_invoice(
    invoice_id: str,
    db: Annotated[Session, Depends(get_db),]
    ) -> GetInvoiceResponse:
    invoice = handle_get_invoice(invoice_id, db)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return invoice

@router.get("", response_model=GetInvoiceListResponse)
async def get_invoices(db: Annotated[Session, Depends(get_db)]) -> GetInvoiceListResponse:
    return handle_get_invoices(db)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=CreateInvoiceResponse)
async def create_invoice(
    request: CreateInvoiceRequest,
    db: Annotated[Session, Depends(get_db)]
    ) -> CreateInvoiceResponse:
    return handle_create_invoice(request, db)

@router.patch("/{invoice_id}", response_model=UpdateInvoiceResponse)
async def update_invoice(
    invoice_id: str,
    request: UpdateInvoiceRequest,
    db: Annotated[Session, Depends(get_db),]
    ) -> GetInvoiceResponse:
    invoice = handle_update_invoice(invoice_id, request, db)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return invoice