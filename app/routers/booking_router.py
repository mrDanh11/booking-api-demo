from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.logger import logger
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.booking_repository import BookingRepository
from app.schemas.booking import BookingDetailResponse, BookingListResponse
from app.services.booking_service import BookingService

router = APIRouter(prefix="/api/v1/bookings", tags=["bookings"])


@router.get(
    "/{booking_no}",
    response_model=BookingDetailResponse,
    summary="Get booking detail by booking number",
)
def get_booking_by_booking_no(
    booking_no: Annotated[
        str,
        Path(
            min_length=5,
            max_length=20,
            pattern=r"^BKG[0-9A-Z]+$",
            description="Booking number, e.g. BKG0012345",
        ),
    ],
    include_containers: Annotated[
        bool,
        Query(description="Whether to include container list in the response"),
    ] = True,
    db: Session = Depends(get_db),
) -> BookingDetailResponse:
    repository = BookingRepository(db)
    service = BookingService(repository)

    try:
        booking = service.get_booking_by_booking_no(
            booking_no=booking_no,
            include_containers=include_containers,
        )
        return booking

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("", response_model=BookingListResponse)
async def list_bookings(
    page: int = Query(default=1, ge=1, description="Page number starting from 1"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    include_containers: bool = Query(
        default=True,
        description="Whether to include container details in each booking",
    ),
    db: Session = Depends(get_db),
) -> BookingListResponse:
    try:
        repository = BookingRepository(db)
        service = BookingService(repository)
        return service.list_bookings(page=page, page_size=page_size, include_containers=include_containers)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error while listing bookings")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
