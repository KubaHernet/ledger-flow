import asyncio
import csv
import io

from ledger_flow.features.invoices.invoices_import.get_import_invoices_template_handler import (
    get_import_invoices_template,
)


def test_get_import_invoices_template_returns_csv_attachment():
    response = get_import_invoices_template()

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert response.headers["content-disposition"] == (
        'attachment; filename="invoice_import_template.csv"'
    )

    async def read_body():
        chunks = []
        async for chunk in response.body_iterator:
            chunks.append(chunk.decode() if isinstance(chunk, bytes) else chunk)
        return "".join(chunks)

    rows = list(csv.reader(io.StringIO(asyncio.run(read_body()))))
    assert rows == [
        [
            "invoice_number",
            "customer_id",
            "issue_date",
            "due_date",
            "amount",
            "currency",
            "status",
        ],
        ["INV-001", "CUS-123", "2026-10-01", "2026-10-31", "1250.50", "EUR", "open"],
    ]
