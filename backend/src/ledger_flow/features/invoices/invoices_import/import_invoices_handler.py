from decimal import Decimal

from fastapi import UploadFile
from ledger_flow.features.invoices.models import Invoice
from ledger_flow.features.invoices.invoices_import.contracts import ImportInvoicesResponse
from sqlalchemy.orm import Session
import csv
import io

async def import_invoices(file: UploadFile, db: Session) -> ImportInvoicesResponse:
    content = await file.read();
    
    text = content.decode("utf-8")
    
    reader = csv.DictReader(io.StringIO(text))
    
    invoices = []
    
    for row in reader:
        invoice = Invoice(
            invoice_number=row["invoice_number"],
            customer_id=row["customer_id"] or None,
            issue_date=row["issue_date"],
            due_date=row["due_date"],
            amount=Decimal(row["amount"]),
            currency=row["currency"],
            status=row.get("status") or "open",
        )
        
        invoices.append(invoice)
        
    db.add_all(invoices)
    db.commit()
    
    return ImportInvoicesResponse(imported_count=len(invoices))