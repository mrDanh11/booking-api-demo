from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.voyage import Voyage


class Vessel(Base):
    __tablename__ = "vessels"

    vessel_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vessel_code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    vessel_name: Mapped[str] = mapped_column(String(100), nullable=False)

    voyages: Mapped[List[Voyage]] = relationship(
        back_populates="vessel",
        cascade="all, delete-orphan",
    )