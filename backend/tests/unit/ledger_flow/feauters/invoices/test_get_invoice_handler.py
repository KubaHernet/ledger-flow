from datetime import date
from decimal import Decimal
from unittest.mock import Mock
from uuid import UUID

from ledger_flow.features.invoices.contracts import GetInvoiceResponse
from ledger_flow.features.invoices.get_invoice_handler import get_invoice
from ledger_flow.features.invoices.models import Invoice


def test_get_invoice_when_exists_returns_invoice():
    # Arrange
    invoice_id = "cc857f48-42fe-4b52-88a7-53c15827ef17"
    db = Mock()
    invoice = Invoice(
        id=UUID(invoice_id),
        invoice_number="INV-001",
        customer_id="some_customer",
        issue_date=date(2026, 11, 4),
        due_date=date(2026, 11, 14),
        amount=Decimal("100.0"),
        currency="PLN",
        status="open",
    )

    db.get.return_value = invoice

    # Act

    result = get_invoice(str(invoice.id), db)

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
