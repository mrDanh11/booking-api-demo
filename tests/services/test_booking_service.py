from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.services.booking_service import BookingService


@pytest.fixture
def booking_repository():
    return Mock()


@pytest.fixture
def booking_service(booking_repository):
    return BookingService(booking_repository)


def make_booking_mock(containers=None):
    """A loose Mock, valid for tests that don't go through pydantic validation."""
    booking = Mock()
    booking.containers = containers if containers is not None else [Mock(), Mock()]
    return booking


def make_booking_data(booking_no="BK001", containers=None):
    """A realistic booking-like object, valid input for BookingDetailResponse.model_validate()."""
    vessel = SimpleNamespace(vessel_id=1, vessel_code="V001", vessel_name="Vessel One")
    voyage = SimpleNamespace(
        voyage_id=1,
        voyage_no="V001",
        origin_port="SGN",
        destination_port="HKG",
        vessel=vessel,
        etd=datetime(2026, 1, 1),
        eta=datetime(2026, 1, 10),
    )
    default_containers = [
        SimpleNamespace(
            container_no="CNT1",
            container_type="20GP",
            seal_no="SEAL1",
            gross_weight=1000.0,
            container_status="LOADED",
        ),
    ]
    return SimpleNamespace(
        booking_no=booking_no,
        customer_name="ACME",
        booking_status="CONFIRMED",
        cargo_description="General cargo",
        created_at=datetime(2026, 1, 1),
        updated_at=datetime(2026, 1, 1),
        voyage=voyage,
        containers=containers if containers is not None else default_containers,
    )


class TestGetBookingByBookingNo:
    def test_returns_booking_with_containers_when_found(self, booking_service, booking_repository):
        booking = make_booking_mock()
        booking_repository.get_booking_by_booking_no.return_value = booking

        result = booking_service.get_booking_by_booking_no("BK001", include_containers=True)

        assert result is booking
        assert result.containers == booking.containers
        booking_repository.get_booking_by_booking_no.assert_called_once_with("BK001", True)

    def test_clears_containers_when_include_containers_false(self, booking_service, booking_repository):
        booking = make_booking_mock()
        booking_repository.get_booking_by_booking_no.return_value = booking

        result = booking_service.get_booking_by_booking_no("BK001", include_containers=False)

        assert result.containers == []
        booking_repository.get_booking_by_booking_no.assert_called_once_with("BK001", False)

    def test_raises_404_when_booking_not_found(self, booking_service, booking_repository):
        booking_repository.get_booking_by_booking_no.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            booking_service.get_booking_by_booking_no("MISSING")

        assert exc_info.value.status_code == 404
        assert "MISSING" in exc_info.value.detail

    def test_defaults_to_include_containers_true(self, booking_service, booking_repository):
        booking_repository.get_booking_by_booking_no.return_value = make_booking_mock()

        booking_service.get_booking_by_booking_no("BK001")

        booking_repository.get_booking_by_booking_no.assert_called_once_with("BK001", True)


class TestListBookings:
    def test_returns_paginated_response_with_containers(self, booking_service, booking_repository):
        items = [make_booking_data("BK001"), make_booking_data("BK002")]
        booking_repository.list_bookings.return_value = (items, 2)

        result = booking_service.list_bookings(page=1, page_size=10, include_containers=True)

        assert [item.booking_no for item in result.items] == ["BK001", "BK002"]
        assert all(len(item.containers) == 1 for item in result.items)
        assert result.total == 2
        assert result.page == 1
        assert result.page_size == 10
        assert result.total_pages == 1
        booking_repository.list_bookings.assert_called_once_with(1, 10, True)

    def test_clears_containers_for_each_item_when_include_containers_false(
        self, booking_service, booking_repository
    ):
        items = [make_booking_data("BK001"), make_booking_data("BK002")]
        booking_repository.list_bookings.return_value = (items, 2)

        result = booking_service.list_bookings(page=1, page_size=10, include_containers=False)

        assert all(item.containers == [] for item in result.items)

    def test_total_pages_rounds_up(self, booking_service, booking_repository):
        booking_repository.list_bookings.return_value = ([], 25)

        result = booking_service.list_bookings(page=1, page_size=10)

        assert result.total_pages == 3

    def test_total_pages_zero_when_no_results(self, booking_service, booking_repository):
        booking_repository.list_bookings.return_value = ([], 0)

        result = booking_service.list_bookings(page=1, page_size=10)

        assert result.total_pages == 0
