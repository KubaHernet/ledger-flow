from pydantic import BaseModel


class ImportInvoicesResponse(BaseModel):
    imported_count: int