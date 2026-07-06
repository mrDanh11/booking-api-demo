from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.booking import Booking


class Container(Base):
    __tablename__ = "containers"

    container_no: Mapped[str] = mapped_column(String(20), primary_key=True)
    booking_no: Mapped[str] = mapped_column(ForeignKey("bookings.booking_no"), nullable=False)
    container_type: Mapped[str] = mapped_column(String(10), nullable=False)
    seal_no: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    gross_weight: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)
    container_status: Mapped[str] = mapped_column(String(20), nullable=False, default="EMPTY")

    booking: Mapped[Booking] = relationship(back_populates="containers")