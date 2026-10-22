# SQLAlchemy CRUD: invoices

These examples follow the invoice handlers in this project. Each function receives a SQLAlchemy `Session` (`db`) and uses the `Invoice` model.

```python
from sqlalchemy.orm import Session
from ledger_flow.features.invoices.models import Invoice
```

### Get all items

```python
invoices = db.query(Invoice).all()
```

`all()` returns a list; it will be empty if there are no invoices.

### Get one item by ID

```python
invoice = db.get(Invoice, invoice_id)
if invoice is None:
    return None
```

`db.get()` returns the matching invoice or `None` when it does not exist.

### Add a new item

```python
invoice = Invoice(
    invoice_number=request.invoice_number,
    customer_id=request.customer_id,
    issue_date=request.issue_date,
    due_date=request.due_date,
    amount=request.amount,
    currency=request.currency,
    status=request.status,
)
db.add(invoice)
db.commit()
db.refresh(invoice)
```

`add()` stages the new object, `commit()` saves it, and `refresh()` loads generated values such as its ID.

### Update an item

```python
invoice = db.get(Invoice, invoice_id)
if invoice is None:
    return None

for field, value in request.model_dump(exclude_unset=True).items():
    setattr(invoice, field, value)

db.commit()
db.refresh(invoice)
```

`exclude_unset=True` updates only fields supplied in the request. `setattr()` assigns each value to the matching model field.
