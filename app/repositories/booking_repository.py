from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, noload, selectinload

from app.models.booking import Booking
from app.models.voyage import Voyage


class BookingRepository:
    def __init__(self, db):
        self.db = db

    def get_booking_by_booking_no(self, booking_no: str, include_containers: bool = True):
        stmt = (
            select(Booking)
            .where(Booking.booking_no == booking_no)
            .options(joinedload(Booking.voyage).joinedload(Voyage.vessel))
        )

        if include_containers:
            stmt = stmt.options(selectinload(Booking.containers))
        else:
            stmt = stmt.options(noload(Booking.containers))

        result = self.db.execute(stmt)
        
        if include_containers:
            return result.unique().scalar_one_or_none()

        return result.scalar_one_or_none()

    def list_bookings(self, page: int, page_size: int, include_containers: bool = True):
        total = self.db.execute(select(func.count()).select_from(Booking)).scalar_one()

        stmt = (
            select(Booking)
            .options(joinedload(Booking.voyage).joinedload(Voyage.vessel))
            .order_by(Booking.booking_no)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        if include_containers:
            stmt = stmt.options(selectinload(Booking.containers))
        else:
            stmt = stmt.options(noload(Booking.containers))

        result = self.db.execute(stmt)
        items = result.unique().scalars().all()

        return items, total