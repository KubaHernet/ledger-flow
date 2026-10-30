```python
import csv
import io

from fastapi.responses import StreamingResponse


def get_import_invoices_template() -> StreamingResponse:
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        "invoice_number",
        "customer_id",
        "issue_date",
        "due_date",
        "amount",
        "currency",
        "status",
    ])
    
    writer.writerow([
        "INV-001",
        "CUS-123",
        "2026-10-01",
        "2026-10-31",
        "1250.50",
        "EUR",
        "open",
    ])
    
    # set stream position to begining
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition":
                'attachment; filename="invoice_import_template.csv"'
        },
    )
```