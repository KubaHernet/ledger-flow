import asyncio
from io import BytesIO
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import UploadFile

from ledger_flow.features.invoices.invoices_import.contracts import ImportInvoiceRow
from ledger_flow.features.invoices.invoices_import.import_invoices_handler import (
    import_invoices,
)
from ledger_flow.features.invoices.models import Invoice

PARSER = (
    "ledger_flow.features.invoices.invoices_import."
    "import_invoices_handler.parse_invoices_csv"
)


@pytest.mark.parametrize("count", [0, 1, 2])
def test_import_invoices_persists_parsed_rows_and_returns_count(db, invoice, count):
    rows = [
        ImportInvoiceRow(
            invoice_number=f"INV-{index}",
            customer_name="Example customer",
            customer_id=invoice.customer_id,
            issue_date=invoice.issue_date,
            due_date=invoice.due_date,
            amount=invoice.amount,
            currency=invoice.currency,
            status="paid",
        )
        for index in range(count)
    ]
    file = UploadFile(filename="invoices.csv", file=BytesIO())
    with patch(PARSER, new_callable=AsyncMock, return_value=rows) as parser:
        result = asyncio.run(import_invoices(file, db))

    parser.assert_awaited_once_with(file)
    assert result.imported_count == count
    db.add_all.assert_called_once()
    saved = db.add_all.call_args.args[0]
    assert len(saved) == count
    for entity, row in zip(saved, rows, strict=True):
        assert isinstance(entity, Invoice)
        for field, expected in row.model_dump(exclude={"customer_name"}).items():
            assert getattr(entity, field) == expected
    db.commit.assert_called_once_with()


def test_import_invoices_when_parsing_fails_does_not_write(db):
    file = UploadFile(filename="invalid.csv", file=BytesIO())
    with (
        patch(PARSER, new_callable=AsyncMock, side_effect=ValueError("invalid CSV")),
        pytest.raises(ValueError, match="invalid CSV"),
    ):
        asyncio.run(import_invoices(file, db))

    db.add_all.assert_not_called()
    db.commit.assert_not_called()


def test_import_invoices_propagates_commit_failure(db):
    file = UploadFile(filename="invoices.csv", file=BytesIO())
    db.commit.side_effect = RuntimeError("commit failed")
    with (
        patch(PARSER, new_callable=AsyncMock, return_value=[]),
        pytest.raises(RuntimeError, match="commit failed"),
    ):
        asyncio.run(import_invoices(file, db))
