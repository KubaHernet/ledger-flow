from unittest.mock import call

import pytest

from ledger_flow.features.invoices.contracts import CreateInvoiceRequest
from ledger_flow.features.invoices.create_invoice_handler import create_invoice
from ledger_flow.features.invoices.models import Invoice


@pytest.mark.parametrize("customer_id", ["CUS-123", None])
def test_create_invoice_persists_request_and_returns_generated_id(
    db, invoice, customer_id
):
    request = CreateInvoiceRequest(
        invoice_number=invoice.invoice_number,
        customer_id=customer_id,
        issue_date=invoice.issue_date,
        due_date=invoice.due_date,
        amount=invoice.amount,
        currency=invoice.currency,
        status="paid",
    )

    def assign_id(entity):
        entity.id = invoice.id

    db.refresh.side_effect = assign_id

    result = create_invoice(request, db)

    saved = db.add.call_args.args[0]
    assert isinstance(saved, Invoice)
    for field, expected in request.model_dump().items():
        assert getattr(saved, field) == expected
    assert result.invoice_id == invoice.id
    assert db.method_calls == [call.add(saved), call.commit(), call.refresh(saved)]


def test_create_invoice_propagates_commit_failure_without_refreshing(db, invoice):
    request = CreateInvoiceRequest(
        invoice_number=invoice.invoice_number,
        issue_date=invoice.issue_date,
        due_date=invoice.due_date,
        amount=invoice.amount,
        currency=invoice.currency,
    )
    db.commit.side_effect = RuntimeError("commit failed")

    with pytest.raises(RuntimeError, match="commit failed"):
        create_invoice(request, db)

    db.refresh.assert_not_called()
