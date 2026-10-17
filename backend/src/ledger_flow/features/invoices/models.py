from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Date, Numeric, String

from ledger_flow.database import EntityBase
from sqlalchemy.orm import Mapped, mapped_column

class Invoice(EntityBase):
    __tablename__ = "invoices"
    
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )
    
    invoice_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    
    customer_id: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )
    
    issue_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
    
    due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
    
    amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False
    )
    
    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False
    )
    
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )
