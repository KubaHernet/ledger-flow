from sqlalchemy.orm import Session
from ledger_flow.features.invoices.models import Invoice
from ledger_flow.features.invoices.contracts import CreateInvoiceRequest, CreateInvoiceResponse


def create_invoice(
    request : CreateInvoiceRequest,
    db: Session
) -> CreateInvoiceResponse:
    invoice = Invoice(
        invoice_number = request.invoice_number,
        customer_id = request.customer_id,
        issue_date = request.issue_date,
        due_date = request.due_date,
        amount = request.amount,
        currency = request.amount,
        status = request.status
    )
    
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    
    return CreateInvoiceResponse(
        invoice_id = invoice.id
    )
    