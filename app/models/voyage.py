from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.vessel import Vessel


class Voyage(Base):
    __tablename__ = "voyages"
    __table_args__ = (
        UniqueConstraint("vessel_id", "voyage_no", name="uq_voyages_vessel_id_voyage_no"),
    )

    voyage_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vessel_id: Mapped[int] = mapped_column(ForeignKey("vessels.vessel_id"), nullable=False)
    voyage_no: Mapped[str] = mapped_column(String(20), nullable=False)
    origin_port: Mapped[str] = mapped_column(String(10), nullable=False)
    destination_port: Mapped[str] = mapped_column(String(10), nullable=False)
    etd: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    eta: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    vessel: Mapped[Vessel] = relationship(back_populates="voyages")
    bookings: Mapped[List[Booking]] = relationship(
        back_populates="voyage",
        cascade="all, delete-orphan",
    )