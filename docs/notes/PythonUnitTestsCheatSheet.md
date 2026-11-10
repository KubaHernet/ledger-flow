# Python Unit Testing Cheat Sheet

This project uses **pytest** to run tests and Python's built-in **unittest.mock** to replace dependencies.

A unit test checks a small piece of behavior in isolation, such as an invoice handler. Mocking its database session lets you test it without connecting to PostgreSQL. An integration test checks real components working together, such as a handler and a database.

## 1. A simple test

Name test files `test_*.py` and test functions `test_*` so pytest discovers them.

```python
def add(a, b):
    return a + b


def test_add_returns_sum():
    # Arrange: prepare inputs.
    first = 2
    second = 3

    # Act: execute the behavior being tested.
    result = add(first, second)

    # Assert: check the expected outcome.
    assert result == 5
```

In a real project, import the function from application code instead of defining it in the test file. Arrange / Act / Assert is a useful structure; the comments are optional.

## 2. Assertions

An assertion fails the test when its condition is false. Pytest shows the failing expression and the values involved.

```python
assert result == expected       # Equal values
assert result != unexpected     # Different values
assert result is None           # Exactly None
assert result is not None
assert result is True           # Exactly the boolean True
assert result                   # Truthy: also accepts nonempty lists, etc.
assert len(items) == 2
assert "invoice_id" in data
assert items == []
```

Use `==` to compare values and `is` for identity, especially `None`. Prefer precise checks such as `assert result == []` when an exact value matters.

For money, use `Decimal("1250.50")` instead of floating-point numbers.

## 3. Run tests from PowerShell

Start in the backend folder and activate its virtual environment:

```powershell
cd C:\repos\ledger-flow\backend
.\.venv\Scripts\Activate.ps1
```

The commands below assume that working directory. `python -m pytest` uses pytest installed for the selected Python interpreter. The project config in `pyproject.toml` sets `tests` as the test directory and adds `src` to the Python import path.

Run **one test function**:

```powershell
python -m pytest tests/unit/ledger_flow/feauters/invoices/test_create_invoice_handler.py::test_create_invoice_persists_request_and_returns_generated_id -v
```

Run **one test file**:

```powershell
python -m pytest tests/unit/ledger_flow/feauters/invoices/test_create_invoice_handler.py -v
```

Run **a folder**, including its subfolders:

```powershell
python -m pytest tests/unit/ledger_flow/feauters/invoices -v
```

Run **all unit tests**:

```powershell
python -m pytest tests/unit -v
```

Run **all discovered tests**:

```powershell
python -m pytest
```

`feauters` is the current spelling of the tests folder in this repository.

Useful options:

| Option | Purpose |
| --- | --- |
| `-v` | Show individual test names |
| `-q` | Less output |
| `-k "create_invoice"` | Select tests whose names match an expression |
| `-x` | Stop after the first failure |
| `--tb=short` | Shorter failure tracebacks |
| `-s` | Show print output without capturing it |
| `--collect-only` | List tests without executing them |
| `--lf` | Run previously failed tests, using pytest's cache |
| `-p no:cacheprovider` | Disable pytest's cache, including cache-dependent options |

For the Windows cache permission warning discussed in this project:

```powershell
python -m pytest tests/unit -v -p no:cacheprovider
```

This disables caching for that run. It does not fix folder permissions.

## 4. Mock a dependency

A mock is a controllable replacement for a dependency. It records calls and returns the values you configure.

```python
from unittest.mock import Mock


def load_name(repository, user_id):
    return repository.get_name(user_id)


def test_load_name_returns_repository_result():
    repository = Mock()
    repository.get_name.return_value = "Alice"

    result = load_name(repository, "user-123")

    assert result == "Alice"
    repository.get_name.assert_called_once_with("user-123")
```

`return_value` controls what a call returns. Unconfigured mocks often return more mocks, so explicitly configure values your application reads.

For a SQLAlchemy session:

```python
from unittest.mock import Mock

from sqlalchemy.orm import Session

db = Mock(spec=Session)
db.get.return_value = None
db.query.return_value.all.return_value = []
```

`spec=Session` restricts accessible attribute names to those available on `Session`. It does not enforce method signatures. Use `create_autospec(Session, instance=True)` when you also want call signature checking.

Common mock assertions:

```python
db.commit.assert_called_once_with()       # Exactly once, without arguments
db.add.assert_called_once()              # Exactly once, any arguments
db.get.assert_called_once_with(Invoice, invoice_id)
db.refresh.assert_not_called()
```

Use real request/response objects and model instances where practical. Mock the external dependency, such as the database session, rather than every object in the test.

## 5. Test exceptions

Use `pytest.raises` when an operation should raise an exception:

```python
import pytest


def test_invalid_number_raises_value_error():
    with pytest.raises(ValueError, match="invalid literal"):
        int("not-a-number")
```

The test fails if no exception is raised or if the exception type is wrong. `match` checks the message using a regular expression.

Simulate a dependency failure with `side_effect`:

```python
db.commit.side_effect = RuntimeError("commit failed")

with pytest.raises(RuntimeError, match="commit failed"):
    create_invoice(request, db)

db.refresh.assert_not_called()
```

This verifies that the failure propagates and the handler does not continue to refresh after a failed commit.

## 6. Fixtures and conftest.py

A fixture prepares an object or resource a test needs.

```python
# conftest.py
from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session


@pytest.fixture
def db():
    return Mock(spec=Session)
```

A test requests the fixture by its parameter name:

```python
def test_get_missing_invoice_returns_none(db):
    db.get.return_value = None

    result = get_invoice("cc857f48-42fe-4b52-88a7-53c15827ef17", db)

    assert result is None
```

Here, import `get_invoice` from its application module in the test file. You do not import the `db` fixture: pytest finds it automatically.

Fixtures in `conftest.py` are available to tests in the same directory and its subdirectories. A fixture can also request other fixtures as parameters.

The default scope is **function**: each test execution gets a fresh fixture object. This includes each parametrized case. Within one test execution, repeated requests for that fixture normally use the same object.

Other scopes include `class`, `module`, `package`, and `session`. Shared mutable fixtures need care because one test's changes can affect another. Function scope is a good default for mocks.

For resources needing cleanup, use `yield`:

```python
@pytest.fixture
def resource():
    connection = open_connection()
    try:
        yield connection
    finally:
        connection.close()
```

`open_connection()` is a placeholder for your resource setup. Code after `yield` handles cleanup, including when the test fails.

## 7. Parametrized tests

`@pytest.mark.parametrize` runs one test function with multiple input cases:

```python
import pytest


@pytest.mark.parametrize(
    "first, second, expected",
    [
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
    ],
)
def test_add(first, second, expected):
    assert first + second == expected
```

This produces three separate test results. The parameter names match the function arguments; each tuple supplies one case.

Your invoice test uses:

```python
@pytest.mark.parametrize("customer_id", ["CUS-123", None])
def test_create_invoice_persists_request_and_returns_generated_id(
    db, invoice, customer_id
):
    ...
```

Pytest runs it twice: once with a customer ID and once without one. `db` and `invoice` come from fixtures; `customer_id` comes from the decorator. Each run receives fresh fixture objects.

For readable case names, supply `ids`:

```python
@pytest.mark.parametrize(
    "customer_id",
    ["CUS-123", None],
    ids=["with-customer", "without-customer"],
)
def test_customer_id(customer_id):
    assert customer_id is None or isinstance(customer_id, str)
```

To run just one case, use its collected ID in quotes. For the existing invoice test:

```powershell
python -m pytest "tests/unit/ledger_flow/feauters/invoices/test_create_invoice_handler.py::test_create_invoice_persists_request_and_returns_generated_id[None]" -v
```

Use `--collect-only -q` to see exact case IDs.

## 8. Inspect objects passed to mocks

Your create handler builds an `Invoice` internally. Retrieve that object from the recorded call:

```python
saved = db.add.call_args.args[0]

assert isinstance(saved, Invoice)
assert saved.currency == request.currency
assert saved.amount == request.amount
```

`call_args` describes the most recent call, `.args` contains positional arguments, and `[0]` selects the first argument. Keyword arguments are available through `.kwargs`.

Your test checks all request fields with:

```python
for field, expected in request.model_dump().items():
    assert getattr(saved, field) == expected
```

Pydantic's `model_dump()` returns a dictionary. `getattr(saved, "currency")` reads the same attribute as `saved.currency`.

## 9. Simulate behavior with side_effect

Besides raising exceptions, `side_effect` can execute a function:

```python
def assign_id(entity):
    entity.id = invoice.id


db.refresh.side_effect = assign_id
```

When the handler calls `db.refresh(saved_invoice)`, the mock calls `assign_id(saved_invoice)`. This simulates an ID becoming available after the save/refresh sequence. It does not verify how SQLAlchemy actually generates IDs; that requires an integration test.

An iterable supplies successive return values:

```python
db.get.side_effect = [None, invoice]
```

The first `db.get(...)` returns `None`, and the second returns `invoice`. Further calls raise `StopIteration` once the iterable is exhausted.

## 10. Check call order when it matters

```python
from unittest.mock import call

assert db.method_calls == [
    call.add(saved),
    call.commit(),
    call.refresh(saved),
]
```

This checks the exact sequence, arguments, and absence of extra method calls. Use it when ordering is meaningful. Prefer simpler assertions when internal call order is irrelevant, so harmless refactoring does not break tests.

## 11. Patch an imported dependency

When a dependency is not passed as an argument, `patch` can temporarily replace the name used by the module under test.

The import handler contains:

```python
from ledger_flow.features.invoices.invoices_import.csv_parser import parse_invoices_csv
```

Patch the name in **the handler module that looks it up**:

```python
from unittest.mock import AsyncMock, patch

target = (
    "ledger_flow.features.invoices.invoices_import."
    "import_invoices_handler.parse_invoices_csv"
)

with patch(target, new_callable=AsyncMock, return_value=[]) as parser:
    # Execute the handler here.
    ...
```

Patching only the original function in `csv_parser` would not replace the reference already imported into the handler. The context manager restores the original name when the block ends.

## 12. Async tests and AsyncMock

Use `AsyncMock` for dependencies called with `await`:

```python
import asyncio
from io import BytesIO
from unittest.mock import AsyncMock, patch

from fastapi import UploadFile
from ledger_flow.features.invoices.invoices_import.import_invoices_handler import (
    import_invoices,
)


def test_empty_import(db):
    file = UploadFile(filename="invoices.csv", file=BytesIO())
    target = (
        "ledger_flow.features.invoices.invoices_import."
        "import_invoices_handler.parse_invoices_csv"
    )

    with patch(target, new_callable=AsyncMock, return_value=[]) as parser:
        result = asyncio.run(import_invoices(file, db))

    assert result.imported_count == 0
    parser.assert_awaited_once_with(file)
```

`asyncio.run()` executes the coroutine from a normal synchronous test. This is the approach used in this project's tests and requires no additional pytest async plugin. Do not call it inside an already running event loop.

Checking `assert_awaited_once_with` confirms the async dependency was awaited, rather than merely called.

## 13. Other useful built-in fixtures

| Fixture | Use |
| --- | --- |
| `tmp_path` | A temporary directory unique to the test |
| `monkeypatch` | Temporarily change environment variables or attributes |
| `capsys` | Capture standard output and standard error |

Example with a temporary file:

```python
def test_write_note(tmp_path):
    path = tmp_path / "note.txt"
    path.write_text("Hello", encoding="utf-8")

    assert path.read_text(encoding="utf-8") == "Hello"
```

Example with an environment variable:

```python
import os


def test_environment_setting(monkeypatch):
    monkeypatch.setenv("EXAMPLE_MODE", "test")

    assert os.getenv("EXAMPLE_MODE") == "test"
```

`monkeypatch` restores its changes after the test. If application code reads an environment variable during import, changing the variable afterward does not update the value already stored in that module.

## 14. Coverage and code checks

The project's development dependencies include `pytest-cov` and Ruff.

```powershell
python -m pytest tests/unit --cov=ledger_flow.features.invoices --cov-report=term-missing -p no:cacheprovider
python -m ruff check .
python -m ruff format --check .
```

Coverage shows which statements executed. Add `--cov-branch` to measure branches too. Even 100% coverage does not prove correctness: useful assertions and realistic cases still matter.

## 15. Choosing useful test cases

For a handler, consider:

- A normal successful request and the returned values.
- Missing records and empty collections.
- Optional fields present and absent.
- Partial updates preserving fields that were not supplied.
- Dependency failures and operations that must not happen afterward.
- Boundary inputs relevant to the behavior.

Keep tests independent, use predictable dates and IDs, and avoid real network/database calls in unit tests. Separate request validation tests from handler tests when validation belongs to the Pydantic request model.

A mocked session cannot prove that a database transaction works, constraints are enforced, or SQL queries are valid. Add integration tests for those behaviors. Similarly, handler tests do not verify HTTP routing, status codes, or that a downloaded CSV can be imported successfully; those need their own tests.

When a test fails, first read the assertion and actual values, then check whether the application behavior or the test expectation is wrong. Avoid changing expectations simply to make a failing test pass.
