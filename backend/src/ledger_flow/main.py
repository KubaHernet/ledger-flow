import uuid

from fastapi import FastAPI

from ledger_flow.features.invoices.router import router as invoices_router

app = FastAPI()

app.include_router(invoices_router)

@app.get("/health")
def health():
    return {"status": "ok"}