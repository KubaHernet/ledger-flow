from ledger_flow.features.invoices.contracts import GetInvoiceResponse
from ledger_flow.features.invoices.models import Invoice
from sqlalchemy.orm import Session

def get_invoice(
    invoice_id: str,
    db: Session
) -> GetInvoiceResponse:
    invoice = db.get(Invoice, invoice_id)
    
    if(invoice is None):
        return None
    
    return GetInvoiceResponse(
        invoice_id = invoice_id,
        invoice_number = invoice.invoice_number,
        customer_id = invoice.customer_id,
        issue_date = invoice.issue_date,
        due_date = invoice.due_date,
        amount = invoice.amount,
        currency = invoice.currency,
        status = invoice.status
    )