from ledger_flow.features.invoices.contracts import InvoiceResponseItem
from ledger_flow.features.invoices.get_invoices_handler import get_invoices
from ledger_flow.features.invoices.models import Invoice


def test_get_invoices_returns_all_fields_in_query_order(db, invoice):
    second = Invoice(
        **{
            field: getattr(invoice, field)
            for field in (
                "customer_id",
                "issue_date",
                "due_date",
                "amount",
                "currency",
                "status",
            )
        },
        id="48ea2fc9-6fab-47a4-b5f2-6066e1222155",
        invoice_number="INV-002",
    )
    db.query.return_value.all.return_value = [invoice, second]

    result = get_invoices(db)

    assert result.invoices == [
        InvoiceResponseItem(
            invoice_id=item.id,
            **{
                field: getattr(item, field)
                for field in (
                    "invoice_number",
                    "customer_id",
                    "issue_date",
                    "due_date",
                    "amount",
                    "currency",
                    "status",
                )
            },
        )
        for item in [invoice, second]
    ]
    db.query.assert_called_once_with(Invoice)
    db.query.return_value.all.assert_called_once_with()


def test_get_invoices_when_empty_returns_empty_list(db):
    db.query.return_value.all.return_value = []

    assert get_invoices(db).invoices == []
