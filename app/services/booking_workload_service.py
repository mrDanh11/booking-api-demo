import math
from decimal import Decimal
from typing import Any, Dict, List, Optional

from fastapi import HTTPException

from app.repositories.booking_workload_repository import BookingWorkloadRepository
from app.schemas import booking_workload as schemas


class BookingWorkloadService:
    def __init__(self, repository: BookingWorkloadRepository):
        self.repository = repository

    def get_booking_workload_summary(
        self,
        office_code: str,
        minutes: int,
        booking_status: Optional[str],
        container_status: Optional[str],
        include_attention_only: bool,
        sort_by: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ) -> schemas.BookingWorkloadResponse:
        office_row = self.repository.get_office_by_code(office_code)
        if office_row is None:
            raise HTTPException(status_code=404, detail="Office not found")

        # Unpaginated: the full matching set, used both for summary totals
        # and as the source to slice a page from further down.
        booking_rows = self.repository.get_booking_workload_rows(
            office_code=office_code,
            minutes=minutes,
            booking_status=booking_status,
            container_status=container_status,
            include_attention_only=include_attention_only,
            sort_by=sort_by,
        )
        operation_status_rows = self.repository.get_operation_status_summary_rows(
            office_code=office_code,
            minutes=minutes,
            booking_status=booking_status,
            container_status=container_status,
            include_attention_only=include_attention_only,
        )
        container_status_rows = self.repository.get_container_status_summary_rows(
            office_code=office_code,
            minutes=minutes,
            booking_status=booking_status,
            container_status=container_status,
            include_attention_only=include_attention_only,
        )

        return schemas.BookingWorkloadResponse(
            office=schemas.OfficeInfoResponse.model_validate(office_row),
            filters=schemas.BookingWorkloadFiltersResponse(
                minutes=minutes,
                booking_status=booking_status,
                container_status=container_status,
                include_attention_only=include_attention_only,
                sort_by=sort_by,
            ),
            summary=self._build_summary(booking_rows),
            operation_status_summary=[
                schemas.OperationStatusSummaryItem.model_validate(row) for row in operation_status_rows
            ],
            container_status_summary=[
                schemas.ContainerStatusSummaryItem.model_validate(row) for row in container_status_rows
            ],
            pagination=self._build_pagination(booking_rows, page, page_size),
            bookings=[self._map_booking_row(row) for row in self._paginate(booking_rows, page, page_size)],
        )

    def _paginate(self, booking_rows: List[Dict[str, Any]], page: int, page_size: int) -> List[Dict[str, Any]]:
        start = (page - 1) * page_size
        return booking_rows[start : start + page_size]

    def _build_pagination(
        self, booking_rows: List[Dict[str, Any]], page: int, page_size: int
    ) -> schemas.BookingWorkloadPaginationResponse:
        total_items = len(booking_rows)
        total_pages = math.ceil(total_items / page_size) if total_items else 0
        return schemas.BookingWorkloadPaginationResponse(
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
        )

    def _build_summary(self, booking_rows: List[Dict[str, Any]]) -> schemas.BookingWorkloadSummaryResponse:
        total_gross_weight = sum(
            (row["total_gross_weight"] for row in booking_rows), Decimal("0")
        )
        return schemas.BookingWorkloadSummaryResponse(
            total_booking_count=len(booking_rows),
            total_container_count=sum(row["container_count"] for row in booking_rows),
            total_gross_weight=total_gross_weight,
            attention_booking_count=sum(1 for row in booking_rows if row["needs_attention"]),
        )

    def _map_booking_row(self, row: Dict[str, Any]) -> schemas.BookingWorkloadItemResponse:
        return schemas.BookingWorkloadItemResponse(
            booking_no=row["booking_no"],
            customer_name=row["customer_name"],
            booking_status=row["booking_status"],
            operation_status=row["operation_status"],
            export_ready=row["operation_status"] == "READY",
            route=schemas.BookingRouteResponse(
                origin_port=row["origin_port"],
                destination_port=row["destination_port"],
            ),
            vessel=schemas.BookingVesselWorkloadResponse(
                vessel_id=row["vessel_id"],
                vessel_code=row["vessel_code"],
                vessel_name=row["vessel_name"],
                voyage_no=row["voyage_no"],
            ),
            container_summary=schemas.BookingContainerSummaryResponse(
                container_count=row["container_count"],
                total_gross_weight=row["total_gross_weight"],
                status_count=schemas.BookingContainerStatusCountResponse(
                    empty=row["empty_count"],
                    gate_in=row["gate_in_count"],
                    loaded=row["loaded_count"],
                    discharged=row["discharged_count"],
                    delivered=row["delivered_count"],
                ),
            ),
            data_quality=schemas.BookingDataQualityResponse(
                missing_container=row["container_count"] == 0,
                needs_attention=row["needs_attention"],
            ),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
