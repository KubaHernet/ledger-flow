from decimal import Decimal

from fastapi import UploadFile
from ledger_flow.features.invoices.invoices_import.csv_parser import parse_invoices_csv
from ledger_flow.features.invoices.models import Invoice
from ledger_flow.features.invoices.invoices_import.contracts import ImportInvoicesResponse
from sqlalchemy.orm import Session

async def import_invoices(file: UploadFile, db: Session) -> ImportInvoicesResponse:
    rows = await parse_invoices_csv(file)

    invoices = [
        Invoice(
            invoice_number=row.invoice_number,
            customer_name=row.customer_name,
            customer_id=row.customer_id,
            issue_date=row.issue_date,
            due_date=row.due_date,
            amount=row.amount,
            currency=row.currency,
            status=row.status
        )
        for row in rows
    ]

    db.add_all(invoices)
    db.commit()

    return ImportInvoicesResponse(
        imported_count=len(invoices),
    )