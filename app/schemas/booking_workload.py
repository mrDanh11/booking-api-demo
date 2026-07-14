from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class BookingStatusFilter(str, Enum):
    CONFIRMED = "CONFIRMED"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


class ContainerStatusFilter(str, Enum):
    EMPTY = "EMPTY"
    GATE_IN = "GATE_IN"
    LOADED = "LOADED"
    DISCHARGED = "DISCHARGED"
    DELIVERED = "DELIVERED"


class BookingSortByFilter(str, Enum):
    UPDATED_AT = "updated_at"
    BOOKING_NO = "booking_no"
    OPERATION_STATUS = "operation_status"


class OfficeInfoResponse(BaseModel):
    office_code: str = Field(description="Handling office code, e.g. RICHQ")
    office_name: str = Field(description="Human-readable name of the handling office")

    model_config = ConfigDict(from_attributes=True)


class BookingWorkloadFiltersResponse(BaseModel):
    minutes: int = Field(default=1440, description="Lookback period in minutes that was applied")
    booking_status: Optional[str] = Field(default=None, description="booking_status filter that was applied, if any")
    container_status: Optional[str] = Field(default=None, description="container_status filter that was applied, if any")
    include_attention_only: bool = Field(default=False, description="Whether only attention-needing bookings were requested")
    sort_by: Optional[str] = Field(default=None, description="Field the bookings array was sorted by, if any")

    model_config = ConfigDict(from_attributes=True)


class BookingWorkloadSummaryResponse(BaseModel):
    total_booking_count: int = Field(description="Total number of bookings matching the filters")
    total_container_count: int = Field(description="Total number of containers across all matching bookings")
    total_gross_weight: Decimal = Field(description="Sum of container gross weight across all matching bookings")
    attention_booking_count: int = Field(description="Number of matching bookings with needs_attention = true")

    model_config = ConfigDict(from_attributes=True)


class OperationStatusSummaryItem(BaseModel):
    operation_status: str = Field(description="Derived operation status, e.g. READY, NEEDS_CONTAINER, PENDING")
    booking_count: int = Field(description="Number of bookings in this operation status")
    container_count: int = Field(description="Total number of containers across bookings in this operation status")
    total_gross_weight: Decimal = Field(description="Sum of container gross weight for bookings in this operation status")

    model_config = ConfigDict(from_attributes=True)


class ContainerStatusSummaryItem(BaseModel):
    container_status: str = Field(description="Container status, e.g. EMPTY, GATE_IN, LOADED, DISCHARGED, DELIVERED")
    container_count: int = Field(description="Number of containers in this status")

    model_config = ConfigDict(from_attributes=True)


class BookingRouteResponse(BaseModel):
    origin_port: str = Field(description="Origin port code of the booking's voyage")
    destination_port: str = Field(description="Destination port code of the booking's voyage")

    model_config = ConfigDict(from_attributes=True)


class BookingVesselWorkloadResponse(BaseModel):
    vessel_id: int = Field(description="Internal vessel identifier")
    vessel_code: str = Field(description="Vessel code, e.g. ONEAL")
    vessel_name: str = Field(description="Vessel display name, e.g. ONE ALTAIR")
    voyage_no: str = Field(description="Voyage number for this booking, e.g. 001E")

    model_config = ConfigDict(from_attributes=True)


class BookingContainerStatusCountResponse(BaseModel):
    empty: int = Field(description="Number of containers in EMPTY status")
    gate_in: int = Field(description="Number of containers in GATE_IN status")
    loaded: int = Field(description="Number of containers in LOADED status")
    discharged: int = Field(description="Number of containers in DISCHARGED status")
    delivered: int = Field(description="Number of containers in DELIVERED status")

    model_config = ConfigDict(from_attributes=True)


class BookingContainerSummaryResponse(BaseModel):
    container_count: int = Field(description="Total number of containers on this booking")
    total_gross_weight: Decimal = Field(description="Sum of gross weight across this booking's containers")
    status_count: BookingContainerStatusCountResponse = Field(description="Container count broken down by status")

    model_config = ConfigDict(from_attributes=True)


class BookingDataQualityResponse(BaseModel):
    missing_container: bool = Field(description="True when the booking has zero containers")
    needs_attention: bool = Field(description="True when the booking needs operator attention (PENDING or missing containers)")

    model_config = ConfigDict(from_attributes=True)


class BookingWorkloadItemResponse(BaseModel):
    booking_no: str = Field(description="Booking number, e.g. BKG0012345")
    customer_name: str = Field(description="Name of the customer who owns the booking")
    booking_status: str = Field(description="Raw commercial booking status, e.g. CONFIRMED, PENDING")
    operation_status: str = Field(description="Derived operational status (see business rule table)")
    export_ready: bool = Field(description="True when operation_status is READY, i.e. cleared to proceed to the next step")
    route: BookingRouteResponse = Field(description="Origin/destination ports for this booking's voyage")
    vessel: Optional[BookingVesselWorkloadResponse] = Field(default=None, description="Vessel and voyage info for this booking")
    container_summary: BookingContainerSummaryResponse = Field(description="Aggregated container metrics for this booking")
    data_quality: BookingDataQualityResponse = Field(description="Data-quality and attention flags for this booking")

    created_at: datetime = Field(description="Timestamp when the booking was created")
    updated_at: datetime = Field(description="Timestamp when the booking was last updated")

    model_config = ConfigDict(from_attributes=True)


class BookingWorkloadPaginationResponse(BaseModel):
    page: int = Field(description="Current page number, starting from 1")
    page_size: int = Field(description="Number of bookings per page")
    total_items: int = Field(description="Total number of bookings matching the filters, across all pages")
    total_pages: int = Field(description="Total number of pages available")

    model_config = ConfigDict(from_attributes=True)


class BookingWorkloadResponse(BaseModel):
    office: OfficeInfoResponse = Field(description="Handling office this report was requested for")
    filters: BookingWorkloadFiltersResponse = Field(description="Filters that were applied to produce this report")
    summary: BookingWorkloadSummaryResponse = Field(description="Overall totals across all matching bookings")
    operation_status_summary: List[OperationStatusSummaryItem] = Field(description="Booking counts grouped by operation status")
    container_status_summary: List[ContainerStatusSummaryItem] = Field(description="Container counts grouped by container status")
    pagination: BookingWorkloadPaginationResponse = Field(description="Pagination info for the bookings array")
    bookings: List[BookingWorkloadItemResponse] = Field(description="Detailed list of bookings matching the filters, for the current page")

    model_config = ConfigDict(from_attributes=True)
