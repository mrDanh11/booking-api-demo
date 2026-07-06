from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class VesselResponse(BaseModel):
    vessel_id: int
    vessel_code: str
    vessel_name: str 

    model_config = ConfigDict(from_attributes=True)

class VoyageResponse(BaseModel):
    voyage_id: int
    voyage_no: str
    origin_port: str
    destination_port: str
    vessel: VesselResponse
    etd: Optional[datetime] = None
    eta: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class ContainerResponse(BaseModel):
    container_no: str
    container_type: str
    seal_no: Optional[str] = None
    gross_weight: Optional[float] = None
    container_status: str

    model_config = ConfigDict(from_attributes=True)

class BookingDetailResponse(BaseModel):
    booking_no: str
    customer_name: str
    booking_status: str
    cargo_description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    voyage: VoyageResponse
    containers: list[ContainerResponse] = []

    model_config = ConfigDict(from_attributes=True)

class BookingListResponse(BaseModel):
    items: List[BookingDetailResponse]
    total: int
    page: int
    page_size: int
    total_pages: int