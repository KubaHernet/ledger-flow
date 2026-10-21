from sqlalchemy.orm import Session
from ledger_flow.features.invoices.models import Invoice
from ledger_flow.features.invoices.contracts import UpdateInvoiceRequest, UpdateInvoiceResponse
from uuid import UUID

def update_invoice(
    invoice_id : UUID,
    request : UpdateInvoiceRequest,
        db: Session
) -> UpdateInvoiceResponse | None:
    invoice = db.get(Invoice, invoice_id)
    
    if invoice is None:
        return None
    
    updates = request.model_dump(exclude_unset=True)
    
    for field, value in updates.items():
        setattr(invoice, field, value)
        
    db.commit()
    db.refresh(invoice)

    return UpdateInvoiceResponse(
            invoice_id = invoice_id,
            invoice_number = invoice.invoice_number,
            customer_id = invoice.customer_id,
            issue_date = invoice.issue_date,
            due_date = invoice.due_date,
            amount = invoice.amount,
            currency = invoice.currency,
            status = invoice.status
        )