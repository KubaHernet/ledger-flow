from uuid import UUID

from ledger_flow.features.invoices.contracts import GetInvoiceResponse
from ledger_flow.features.invoices.get_invoice_handler import get_invoice
from ledger_flow.features.invoices.models import Invoice


def test_get_invoice_when_exists_returns_invoice(db, invoice):
    # Arrange
    invoice_id = "cc857f48-42fe-4b52-88a7-53c15827ef17"
    invoice.id = UUID(invoice_id)

    db.get.return_value = invoice

    # Act

    result = get_invoice(invoice_id, db)

    # Assert
    assert result == GetInvoiceResponse(
        invoice_id=invoice.id,
        invoice_number=invoice.invoice_number,
        customer_id=invoice.customer_id,
        issue_date=invoice.issue_date,
        due_date=invoice.due_date,
        amount=invoice.amount,
        currency=invoice.currency,
        status=invoice.status,
    )
    db.get.assert_called_once_with(Invoice, invoice_id)


def test_get_invoice_when_not_exists_returns_none(db):
    # Arrange
    invoice_id = "cc857f48-42fe-4b52-88a7-53c15827ef17"

    db.get.return_value = None

    # Act

    result = get_invoice(str(invoice_id), db)

    # Assert
    assert result is None
    db.get.assert_called_once_with(Invoice, invoice_id)
