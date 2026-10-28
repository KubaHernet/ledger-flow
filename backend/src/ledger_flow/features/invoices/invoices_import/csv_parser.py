import csv
import io

from fastapi import UploadFile
from ledger_flow.features.invoices.invoices_import.contracts import ImportInvoiceRow


async def parse_invoices_csv(file: UploadFile):
    content = await file.read();
        
    text = content.decode("utf-8")
    
    reader = csv.DictReader(io.StringIO(text))
    
    invoices = []
    
    for row in reader:
        invoices.append(
            ImportInvoiceRow.model_validate(row)
        )
        
    return invoices