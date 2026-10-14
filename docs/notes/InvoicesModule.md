I have initialized invoices module - created a directory /features/invoices

added create invoice request model - to be verified if it's correct 

added fast api router 
```
from fastapi import APIRouter, status
from uuid import uuid4
from ledger_flow.features.invoices.contracts import CreateInvoiceRequest, CreateInvoiceResponse

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=CreateInvoiceResponse)
async def create_invoice(request: CreateInvoiceRequest):
    response = CreateInvoiceResponse(invoice_id=uuid4())
    return response
```

and registered it in main.py:
```
from fastapi import FastAPI

from ledger_flow.features.invoices.router import router as invoices_router

app = FastAPI()

app.include_router(invoices_router)
```

TODO: 
- add db (postgres?)
