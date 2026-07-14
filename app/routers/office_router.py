from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.logger import logger
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.booking_workload_repository import BookingWorkloadRepository
from app.schemas.booking_workload import (
    BookingSortByFilter,
    BookingStatusFilter,
    BookingWorkloadResponse,
    ContainerStatusFilter,
)
from app.services.booking_workload_service import BookingWorkloadService

router = APIRouter(prefix="/api/v1/offices", tags=["offices"])


@router.get(
    "/{office_code}/booking-workload-summary",
    response_model=BookingWorkloadResponse,
    summary="Get booking workload summary for a handling office",
)
def get_booking_workload_summary(
    office_code: Annotated[
        str,
        Path(
            pattern=r"^[A-Z0-9]{3,10}$",
            description="Handling office code, e.g. RICHQ, SINBB, SGNBB",
        ),
    ],
    minutes: Annotated[
        int,
        Query(ge=1, description="Lookback period in minutes from now"),
    ] = 1440,
    booking_status: Annotated[
        Optional[BookingStatusFilter],
        Query(description="Filter by booking status"),
    ] = None,
    container_status: Annotated[
        Optional[ContainerStatusFilter],
        Query(
            description="Filter bookings that contain at least one container with this status"
        ),
    ] = None,
    include_attention_only: Annotated[
        bool,
        Query(description="Return only bookings that need attention"),
    ] = False,
    sort_by: Annotated[
        Optional[BookingSortByFilter],
        Query(description="Sort the bookings array by this field"),
    ] = None,
    page: Annotated[
        int,
        Query(ge=1, description="Page number of the bookings array, starting from 1"),
    ] = 1,
    page_size: Annotated[
        int,
        Query(ge=1, le=100, description="Number of bookings per page"),
    ] = 10,
    db: Session = Depends(get_db),
) -> BookingWorkloadResponse:
    repository = BookingWorkloadRepository(db)
    service = BookingWorkloadService(repository)

    try:
        return service.get_booking_workload_summary(
            office_code=office_code,
            minutes=minutes,
            booking_status=booking_status.value if booking_status else None,
            container_status=container_status.value if container_status else None,
            include_attention_only=include_attention_only,
            sort_by=sort_by.value if sort_by else None,
            page=page,
            page_size=page_size,
        )
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error while building booking workload summary")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
