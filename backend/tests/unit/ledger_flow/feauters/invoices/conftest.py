from datetime import date
from decimal import Decimal
from unittest.mock import Mock
from uuid import UUID

import pytest
from sqlalchemy.orm import Session

from ledger_flow.features.invoices.models import Invoice


@pytest.fixture
def db():
    return Mock(spec=Session)


@pytest.fixture
def invoice():
    return Invoice(
        id=UUID("cc857f48-42fe-4b52-88a7-53c15827ef17"),
        invoice_number="INV-001",
        customer_id="CUS-123",
        issue_date=date(2026, 11, 1),
        due_date=date(2026, 11, 30),
        amount=Decimal("1250.50"),
        currency="EUR",
        status="open",
    )
