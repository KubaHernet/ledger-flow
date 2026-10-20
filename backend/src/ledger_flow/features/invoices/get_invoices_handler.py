from ledger_flow.features.invoices.models import Invoice
from sqlalchemy.orm import Session

from ledger_flow.features.invoices.contracts import GetInvoiceListResponse, InvoiceResponseItem


def get_invoices(db: Session) -> GetInvoiceListResponse:
    invoices = db.query(Invoice).all()
    
    return GetInvoiceListResponse(
        invoices=[
            InvoiceResponseItem(
                invoice_id=invoice.id,
                invoice_number=invoice.invoice_number,
                customer_id=invoice.customer_id,
                issue_date=invoice.issue_date,
                due_date=invoice.due_date,
                amount=invoice.amount,
                currency=invoice.currency,
                status=invoice.status
            )
            for invoice in invoices
        ]
    )