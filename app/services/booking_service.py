import math

from fastapi import HTTPException

from app.repositories.booking_repository import BookingRepository
from app.schemas.booking import BookingListResponse


class BookingService:
    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository

    def get_booking_by_booking_no(self, booking_no: str, include_containers: bool = True):
        booking = self.booking_repository.get_booking_by_booking_no(booking_no, include_containers)

        if booking is None:
            raise HTTPException(
                status_code=404,
                detail=f"Booking '{booking_no}' not found",
            )
        
        if not include_containers:
            booking.containers = []

        return booking

    def list_bookings(self, page: int, page_size: int, include_containers: bool = True):
        items, total = self.booking_repository.list_bookings(page, page_size, include_containers)

        if not include_containers:
            for booking in items:
                booking.containers = []

        total_pages = math.ceil(total / page_size) if total else 0

        return BookingListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
    
    