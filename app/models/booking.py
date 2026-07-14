from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.container import Container
    from app.models.office import Office
    from app.models.voyage import Voyage


class Booking(Base):
    __tablename__ = "bookings"

    booking_no: Mapped[str] = mapped_column(String(20), primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    voyage_id: Mapped[int] = mapped_column(ForeignKey("voyages.voyage_id"), nullable=False)
    booking_status: Mapped[str] = mapped_column(String(20), nullable=False)
    cargo_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    handling_office: Mapped[Optional[str]] = mapped_column(ForeignKey("offices.office_code"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    voyage: Mapped[Voyage] = relationship(back_populates="bookings")
    containers: Mapped[List[Container]] = relationship(
        back_populates="booking",
        cascade="all, delete-orphan",
        order_by="Container.container_no",
    )
    office: Mapped[Optional["Office"]] = relationship(back_populates="bookings")