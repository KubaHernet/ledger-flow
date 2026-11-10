from datetime import date
from decimal import Decimal
from unittest.mock import call

import pytest

from ledger_flow.features.invoices.contracts import UpdateInvoiceRequest
from ledger_flow.features.invoices.models import Invoice
from ledger_flow.features.invoices.update_incoice_handler import update_invoice


@pytest.mark.parametrize(
    "updates",
    [
        {},
        {"status": "paid"},
        {
            "invoice_number": "INV-UPDATED",
            "customer_id": "CUS-456",
            "issue_date": date(2026, 12, 1),
            "due_date": date(2026, 12, 31),
            "amount": Decimal("999.99"),
            "currency": "PLN",
            "status": "overdue",
        },
    ],
)
def test_update_invoice_applies_only_supplied_fields(db, invoice, updates):
    fields = (
        "invoice_number",
        "customer_id",
        "issue_date",
        "due_date",
        "amount",
        "currency",
        "status",
    )
    expected = {field: getattr(invoice, field) for field in fields} | updates
    db.get.return_value = invoice

    result = update_invoice(invoice.id, UpdateInvoiceRequest(**updates), db)

    assert result.model_dump() == {"invoice_id": invoice.id, **expected}
    assert {field: getattr(invoice, field) for field in fields} == expected
    assert db.method_calls == [
        call.get(Invoice, invoice.id),
        call.commit(),
        call.refresh(invoice),
    ]


def test_update_invoice_when_missing_does_not_write(db, invoice):
    db.get.return_value = None

    assert update_invoice(invoice.id, UpdateInvoiceRequest(status="paid"), db) is None

    db.get.assert_called_once_with(Invoice, invoice.id)
    db.commit.assert_not_called()
    db.refresh.assert_not_called()


def test_update_invoice_propagates_commit_failure(db, invoice):
    db.get.return_value = invoice
    db.commit.side_effect = RuntimeError("commit failed")

    with pytest.raises(RuntimeError, match="commit failed"):
        update_invoice(invoice.id, UpdateInvoiceRequest(status="paid"), db)

    db.refresh.assert_not_called()
