from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.services.booking_workload_service import BookingWorkloadService


@pytest.fixture
def repository():
    return Mock()


@pytest.fixture
def service(repository):
    return BookingWorkloadService(repository)


def make_office_row(office_code="RICHQ", office_name="Richmond Operation Office"):
    return {"office_code": office_code, "office_name": office_name, "country_code": "US"}


def make_booking_row(
    booking_no="BKGW00001",
    booking_status="CONFIRMED",
    operation_status="READY",
    container_count=2,
    total_gross_weight=Decimal("43000.50"),
    empty_count=0,
    gate_in_count=1,
    loaded_count=1,
    discharged_count=0,
    delivered_count=0,
    needs_attention=False,
):
    return {
        "booking_no": booking_no,
        "customer_name": "ABC LOGISTICS",
        "booking_status": booking_status,
        "created_at": datetime(2026, 7, 6, 9, 52, 0),
        "updated_at": datetime(2026, 7, 6, 10, 22, 0),
        "origin_port": "VNSGN",
        "destination_port": "USLAX",
        "vessel_id": 1,
        "vessel_code": "ONEAL",
        "vessel_name": "ONE ALTAIR",
        "voyage_no": "001E",
        "container_count": container_count,
        "total_gross_weight": total_gross_weight,
        "empty_count": empty_count,
        "gate_in_count": gate_in_count,
        "loaded_count": loaded_count,
        "discharged_count": discharged_count,
        "delivered_count": delivered_count,
        "operation_status": operation_status,
        "needs_attention": needs_attention,
    }


class TestOfficeNotFound:
    def test_raises_404_when_office_does_not_exist(self, service, repository):
        repository.get_office_by_code.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            service.get_booking_workload_summary(
                office_code="ZZZZZ",
                minutes=1440,
                booking_status=None,
                container_status=None,
                include_attention_only=False,
            )

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Office not found"
        repository.get_booking_workload_rows.assert_not_called()


class TestSuccessfulResponse:
    def test_builds_response_with_multiple_operation_statuses(self, service, repository):
        repository.get_office_by_code.return_value = make_office_row()
        repository.get_booking_workload_rows.return_value = [
            make_booking_row(booking_no="BKGW00001", operation_status="READY", needs_attention=False),
            make_booking_row(
                booking_no="BKGW00002",
                booking_status="PENDING",
                operation_status="PENDING",
                container_count=0,
                total_gross_weight=Decimal("0"),
                empty_count=0,
                gate_in_count=0,
                loaded_count=0,
                needs_attention=True,
            ),
        ]
        repository.get_operation_status_summary_rows.return_value = [
            {"operation_status": "PENDING", "booking_count": 1, "container_count": 0, "total_gross_weight": Decimal("0")},
            {"operation_status": "READY", "booking_count": 1, "container_count": 2, "total_gross_weight": Decimal("43000.50")},
        ]
        repository.get_container_status_summary_rows.return_value = [
            {"container_status": "GATE_IN", "container_count": 1},
            {"container_status": "LOADED", "container_count": 1},
        ]

        result = service.get_booking_workload_summary(
            office_code="RICHQ",
            minutes=1440,
            booking_status=None,
            container_status=None,
            include_attention_only=False,
        )

        assert result.office.office_code == "RICHQ"
        assert result.office.office_name == "Richmond Operation Office"
        assert result.filters.minutes == 1440
        assert result.summary.total_booking_count == 2
        assert result.summary.total_container_count == 2
        assert result.summary.total_gross_weight == Decimal("43000.50")
        assert result.summary.attention_booking_count == 1
        assert [item.operation_status for item in result.operation_status_summary] == ["PENDING", "READY"]
        assert [item.container_status for item in result.container_status_summary] == ["GATE_IN", "LOADED"]
        assert len(result.bookings) == 2

    def test_passes_filters_through_to_every_repository_call(self, service, repository):
        repository.get_office_by_code.return_value = make_office_row()
        repository.get_booking_workload_rows.return_value = []
        repository.get_operation_status_summary_rows.return_value = []
        repository.get_container_status_summary_rows.return_value = []

        service.get_booking_workload_summary(
            office_code="RICHQ",
            minutes=720,
            booking_status="CONFIRMED",
            container_status="LOADED",
            include_attention_only=True,
            sort_by="updated_at",
        )

        expected_kwargs = {
            "office_code": "RICHQ",
            "minutes": 720,
            "booking_status": "CONFIRMED",
            "container_status": "LOADED",
            "include_attention_only": True,
        }
        # sort_by only affects the detail rows query - the two GROUP BY
        # summary queries don't take it, since they always group by status.
        repository.get_booking_workload_rows.assert_called_once_with(**expected_kwargs, sort_by="updated_at")
        repository.get_operation_status_summary_rows.assert_called_once_with(**expected_kwargs)
        repository.get_container_status_summary_rows.assert_called_once_with(**expected_kwargs)

    def test_filters_echoed_back_in_response(self, service, repository):
        repository.get_office_by_code.return_value = make_office_row()
        repository.get_booking_workload_rows.return_value = []
        repository.get_operation_status_summary_rows.return_value = []
        repository.get_container_status_summary_rows.return_value = []

        result = service.get_booking_workload_summary(
            office_code="RICHQ",
            minutes=720,
            booking_status="CONFIRMED",
            container_status="LOADED",
            include_attention_only=True,
        )

        assert result.filters.minutes == 720
        assert result.filters.booking_status == "CONFIRMED"
        assert result.filters.container_status == "LOADED"
        assert result.filters.include_attention_only is True


class TestEmptyResult:
    def test_returns_zeroed_summary_and_empty_arrays_when_nothing_matches(self, service, repository):
        repository.get_office_by_code.return_value = make_office_row(office_code="SGNBB", office_name="Saigon Booking Office")
        repository.get_booking_workload_rows.return_value = []
        repository.get_operation_status_summary_rows.return_value = []
        repository.get_container_status_summary_rows.return_value = []

        result = service.get_booking_workload_summary(
            office_code="SGNBB",
            minutes=1440,
            booking_status="PENDING",
            container_status=None,
            include_attention_only=False,
        )

        assert result.summary.total_booking_count == 0
        assert result.summary.total_container_count == 0
        assert result.summary.total_gross_weight == Decimal("0")
        assert result.summary.attention_booking_count == 0
        assert result.operation_status_summary == []
        assert result.container_status_summary == []
        assert result.bookings == []


class TestRowMapping:
    def test_maps_flat_row_into_nested_response_fields(self, service, repository):
        repository.get_office_by_code.return_value = make_office_row()
        repository.get_booking_workload_rows.return_value = [
            make_booking_row(
                booking_no="BKGW00013",
                container_count=1,
                total_gross_weight=Decimal("15200.00"),
                empty_count=1,
                gate_in_count=0,
                loaded_count=0,
                discharged_count=0,
                delivered_count=0,
                needs_attention=False,
            )
        ]
        repository.get_operation_status_summary_rows.return_value = []
        repository.get_container_status_summary_rows.return_value = []

        result = service.get_booking_workload_summary(
            office_code="RICHQ",
            minutes=1440,
            booking_status=None,
            container_status=None,
            include_attention_only=False,
        )

        booking = result.bookings[0]
        assert booking.booking_no == "BKGW00013"
        assert booking.route.origin_port == "VNSGN"
        assert booking.route.destination_port == "USLAX"
        assert booking.vessel.vessel_code == "ONEAL"
        assert booking.vessel.voyage_no == "001E"
        assert booking.container_summary.container_count == 1
        assert booking.container_summary.status_count.empty == 1
        assert booking.container_summary.status_count.gate_in == 0
        assert booking.data_quality.needs_attention is False

    def test_missing_container_flag_true_when_container_count_zero(self, service, repository):
        repository.get_office_by_code.return_value = make_office_row()
        repository.get_booking_workload_rows.return_value = [
            make_booking_row(
                booking_no="BKGW00003",
                container_count=0,
                total_gross_weight=Decimal("0"),
                operation_status="NEEDS_CONTAINER",
                needs_attention=True,
            )
        ]
        repository.get_operation_status_summary_rows.return_value = []
        repository.get_container_status_summary_rows.return_value = []

        result = service.get_booking_workload_summary(
            office_code="RICHQ",
            minutes=1440,
            booking_status=None,
            container_status=None,
            include_attention_only=False,
        )

        booking = result.bookings[0]
        assert booking.operation_status == "NEEDS_CONTAINER"
        assert booking.data_quality.missing_container is True
        assert booking.data_quality.needs_attention is True
