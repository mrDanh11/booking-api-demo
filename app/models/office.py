from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.booking import Booking


class Office(Base):
    __tablename__ = "offices"

    office_code: Mapped[str] = mapped_column(String(10), primary_key=True)
    office_name: Mapped[str] = mapped_column(String(100), nullable=False)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False)

    bookings: Mapped[List["Booking"]] = relationship(back_populates="office")
