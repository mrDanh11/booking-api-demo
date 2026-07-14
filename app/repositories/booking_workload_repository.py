from typing import Any, Dict, List, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session


class BookingWorkloadRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_office_by_code(self, office_code: str) -> Optional[Dict[str, Any]]:
        """Check whether the office exists; used to decide the 404 response."""
        query = text("""
            SELECT office_code, office_name, country_code
            FROM offices
            WHERE office_code = :office_code;
        """)

        result = self.db.execute(query, {"office_code": office_code}).mappings().first()
        return dict(result) if result else None

    _SORT_COLUMNS = {
        "updated_at": "updated_at DESC, booking_no",
        "booking_no": "booking_no",
        "operation_status": """
            CASE operation_status
                WHEN 'NEEDS_CONTAINER' THEN 1
                WHEN 'PENDING' THEN 2
                WHEN 'READY' THEN 3
                WHEN 'COMPLETED' THEN 4
                WHEN 'CANCELLED' THEN 5
                ELSE 6
            END, booking_no
        """,
    }

    def get_booking_workload_rows(
        self,
        office_code: str,
        minutes: int,
        booking_status: Optional[str],
        container_status: Optional[str],
        include_attention_only: bool,
        sort_by: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch detailed info for each booking, with nested metrics flattened.
        Used to build the main "bookings": [...] array in the JSON response.
        """
        order_by_clause = self._SORT_COLUMNS.get(sort_by, "needs_attention DESC, updated_at DESC, booking_no")

        query = text(f"""
            WITH container_summary AS (
                SELECT
                    c.booking_no,
                    COUNT(c.container_no) AS container_count,
                    COALESCE(SUM(c.gross_weight), 0) AS total_gross_weight,
                    COUNT(*) FILTER (WHERE c.container_status = 'EMPTY') AS empty_count,
                    COUNT(*) FILTER (WHERE c.container_status = 'GATE_IN') AS gate_in_count,
                    COUNT(*) FILTER (WHERE c.container_status = 'LOADED') AS loaded_count,
                    COUNT(*) FILTER (WHERE c.container_status = 'DISCHARGED') AS discharged_count,
                    COUNT(*) FILTER (WHERE c.container_status = 'DELIVERED') AS delivered_count
                FROM containers c
                GROUP BY c.booking_no
            ),
            booking_base AS (
                SELECT
                    -- Core booking fields
                    b.booking_no,
                    b.customer_name,
                    b.booking_status,
                    b.created_at,
                    b.updated_at,

                    -- Route lives on voyages, not on bookings
                    vo.origin_port,
                    vo.destination_port,

                    -- Vessel fields + voyage number
                    v.vessel_id,
                    v.vessel_code,
                    v.vessel_name,
                    vo.voyage_no,

                    -- Flattened container metrics from container_summary CTE
                    COALESCE(cs.container_count, 0) AS container_count,
                    COALESCE(cs.total_gross_weight, 0) AS total_gross_weight,
                    COALESCE(cs.empty_count, 0) AS empty_count,
                    COALESCE(cs.gate_in_count, 0) AS gate_in_count,
                    COALESCE(cs.loaded_count, 0) AS loaded_count,
                    COALESCE(cs.discharged_count, 0) AS discharged_count,
                    COALESCE(cs.delivered_count, 0) AS delivered_count,

                    -- Derived operation status (see business rule table)
                    CASE
                        WHEN b.booking_status = 'CANCELLED' THEN 'CANCELLED'
                        WHEN b.booking_status = 'COMPLETED' THEN 'COMPLETED'
                        WHEN b.booking_status = 'PENDING' THEN 'PENDING'
                        WHEN b.booking_status = 'CONFIRMED' AND COALESCE(cs.container_count, 0) = 0 THEN 'NEEDS_CONTAINER'
                        WHEN b.booking_status = 'CONFIRMED' THEN 'READY'
                        ELSE 'UNKNOWN'
                    END AS operation_status,

                    -- Derived attention flag
                    CASE
                        WHEN b.booking_status = 'PENDING' THEN TRUE
                        WHEN COALESCE(cs.container_count, 0) = 0 THEN TRUE
                        ELSE FALSE
                    END AS needs_attention
                FROM bookings b
                JOIN voyages vo ON b.voyage_id = vo.voyage_id
                JOIN vessels v ON vo.vessel_id = v.vessel_id
                LEFT JOIN container_summary cs ON b.booking_no = cs.booking_no
                WHERE b.handling_office = :office_code
                  AND b.updated_at >= CURRENT_TIMESTAMP - (:minutes * INTERVAL '1 minute')
            ),
            filtered_booking AS (
                SELECT * FROM booking_base
                WHERE (CAST(:booking_status AS TEXT) IS NULL OR booking_status = CAST(:booking_status AS TEXT))
                  AND (
                      CAST(:container_status AS TEXT) IS NULL
                      OR (CAST(:container_status AS TEXT) = 'EMPTY' AND empty_count > 0)
                      OR (CAST(:container_status AS TEXT) = 'GATE_IN' AND gate_in_count > 0)
                      OR (CAST(:container_status AS TEXT) = 'LOADED' AND loaded_count > 0)
                      OR (CAST(:container_status AS TEXT) = 'DISCHARGED' AND discharged_count > 0)
                      OR (CAST(:container_status AS TEXT) = 'DELIVERED' AND delivered_count > 0)
                  )
                  AND (:include_attention_only = FALSE OR needs_attention = TRUE)
            )
            SELECT * FROM filtered_booking
            ORDER BY {order_by_clause};
        """)

        result = self.db.execute(query, {
            "office_code": office_code,
            "minutes": minutes,
            "booking_status": booking_status,
            "container_status": container_status,
            "include_attention_only": include_attention_only,
        })
        return [dict(row) for row in result.mappings().all()]

    def get_operation_status_summary_rows(
        self,
        office_code: str,
        minutes: int,
        booking_status: Optional[str],
        container_status: Optional[str],
        include_attention_only: bool,
    ) -> List[Dict[str, Any]]:
        """
        Aggregate booking counts grouped by operation status.
        Used for the "operation_status_summary": [...] array in the JSON response.
        The filter set must match get_booking_workload_rows exactly so the totals
        stay consistent with the "bookings" list returned in the same response.
        """
        query = text("""
            WITH container_summary AS (
                SELECT
                    c.booking_no,
                    COUNT(c.container_no) AS container_count,
                    COALESCE(SUM(c.gross_weight), 0) AS total_gross_weight,
                    COUNT(*) FILTER (WHERE c.container_status = 'EMPTY') AS empty_count,
                    COUNT(*) FILTER (WHERE c.container_status = 'GATE_IN') AS gate_in_count,
                    COUNT(*) FILTER (WHERE c.container_status = 'LOADED') AS loaded_count,
                    COUNT(*) FILTER (WHERE c.container_status = 'DISCHARGED') AS discharged_count,
                    COUNT(*) FILTER (WHERE c.container_status = 'DELIVERED') AS delivered_count
                FROM containers c
                GROUP BY c.booking_no
            ),
            booking_base AS (
                SELECT
                    b.booking_no,
                    b.booking_status,
                    COALESCE(cs.container_count, 0) AS container_count,
                    COALESCE(cs.total_gross_weight, 0) AS total_gross_weight,
                    COALESCE(cs.empty_count, 0) AS empty_count,
                    COALESCE(cs.gate_in_count, 0) AS gate_in_count,
                    COALESCE(cs.loaded_count, 0) AS loaded_count,
                    COALESCE(cs.discharged_count, 0) AS discharged_count,
                    COALESCE(cs.delivered_count, 0) AS delivered_count,
                    CASE
                        WHEN b.booking_status = 'CANCELLED' THEN 'CANCELLED'
                        WHEN b.booking_status = 'COMPLETED' THEN 'COMPLETED'
                        WHEN b.booking_status = 'PENDING' THEN 'PENDING'
                        WHEN b.booking_status = 'CONFIRMED' AND COALESCE(cs.container_count, 0) = 0 THEN 'NEEDS_CONTAINER'
                        WHEN b.booking_status = 'CONFIRMED' THEN 'READY'
                        ELSE 'UNKNOWN'
                    END AS operation_status,
                    CASE
                        WHEN b.booking_status = 'PENDING' THEN TRUE
                        WHEN COALESCE(cs.container_count, 0) = 0 THEN TRUE
                        ELSE FALSE
                    END AS needs_attention
                FROM bookings b
                LEFT JOIN container_summary cs ON b.booking_no = cs.booking_no
                WHERE b.handling_office = :office_code
                  AND b.updated_at >= CURRENT_TIMESTAMP - (:minutes * INTERVAL '1 minute')
            ),
            filtered_booking AS (
                SELECT * FROM booking_base
                WHERE (CAST(:booking_status AS TEXT) IS NULL OR booking_status = CAST(:booking_status AS TEXT))
                  AND (
                      CAST(:container_status AS TEXT) IS NULL
                      OR (CAST(:container_status AS TEXT) = 'EMPTY' AND empty_count > 0)
                      OR (CAST(:container_status AS TEXT) = 'GATE_IN' AND gate_in_count > 0)
                      OR (CAST(:container_status AS TEXT) = 'LOADED' AND loaded_count > 0)
                      OR (CAST(:container_status AS TEXT) = 'DISCHARGED' AND discharged_count > 0)
                      OR (CAST(:container_status AS TEXT) = 'DELIVERED' AND delivered_count > 0)
                  )
                  AND (:include_attention_only = FALSE OR needs_attention = TRUE)
            )
            SELECT
                operation_status,
                COUNT(*) AS booking_count,
                SUM(container_count) AS container_count,
                COALESCE(SUM(total_gross_weight), 0) AS total_gross_weight
            FROM filtered_booking
            GROUP BY operation_status
            ORDER BY operation_status;
        """)

        result = self.db.execute(query, {
            "office_code": office_code,
            "minutes": minutes,
            "booking_status": booking_status,
            "container_status": container_status,
            "include_attention_only": include_attention_only,
        })
        return [dict(row) for row in result.mappings().all()]

    def get_container_status_summary_rows(
        self,
        office_code: str,
        minutes: int,
        booking_status: Optional[str],
        container_status: Optional[str],
        include_attention_only: bool,
    ) -> List[Dict[str, Any]]:
        """
        Aggregate container counts grouped by container status.
        Used for the "container_status_summary": [...] array in the JSON response.
        container_status is only used to pick the right set of bookings (same as
        the other two methods); the final GROUP BY still returns the full status
        breakdown for that set of bookings, not just the filtered status.
        """
        query = text("""
            WITH container_summary AS (
                SELECT
                    c.booking_no,
                    COUNT(c.container_no) AS container_count,
                    COUNT(*) FILTER (WHERE c.container_status = 'EMPTY') AS empty_count,
                    COUNT(*) FILTER (WHERE c.container_status = 'GATE_IN') AS gate_in_count,
                    COUNT(*) FILTER (WHERE c.container_status = 'LOADED') AS loaded_count,
                    COUNT(*) FILTER (WHERE c.container_status = 'DISCHARGED') AS discharged_count,
                    COUNT(*) FILTER (WHERE c.container_status = 'DELIVERED') AS delivered_count
                FROM containers c
                GROUP BY c.booking_no
            ),
            booking_base AS (
                SELECT
                    b.booking_no,
                    b.booking_status,
                    COALESCE(cs.container_count, 0) AS container_count,
                    COALESCE(cs.empty_count, 0) AS empty_count,
                    COALESCE(cs.gate_in_count, 0) AS gate_in_count,
                    COALESCE(cs.loaded_count, 0) AS loaded_count,
                    COALESCE(cs.discharged_count, 0) AS discharged_count,
                    COALESCE(cs.delivered_count, 0) AS delivered_count,
                    CASE
                        WHEN b.booking_status = 'PENDING' THEN TRUE
                        WHEN COALESCE(cs.container_count, 0) = 0 THEN TRUE
                        ELSE FALSE
                    END AS needs_attention
                FROM bookings b
                LEFT JOIN container_summary cs ON b.booking_no = cs.booking_no
                WHERE b.handling_office = :office_code
                  AND b.updated_at >= CURRENT_TIMESTAMP - (:minutes * INTERVAL '1 minute')
            ),
            filtered_booking AS (
                SELECT booking_no FROM booking_base
                WHERE (CAST(:booking_status AS TEXT) IS NULL OR booking_status = CAST(:booking_status AS TEXT))
                  AND (
                      CAST(:container_status AS TEXT) IS NULL
                      OR (CAST(:container_status AS TEXT) = 'EMPTY' AND empty_count > 0)
                      OR (CAST(:container_status AS TEXT) = 'GATE_IN' AND gate_in_count > 0)
                      OR (CAST(:container_status AS TEXT) = 'LOADED' AND loaded_count > 0)
                      OR (CAST(:container_status AS TEXT) = 'DISCHARGED' AND discharged_count > 0)
                      OR (CAST(:container_status AS TEXT) = 'DELIVERED' AND delivered_count > 0)
                  )
                  AND (:include_attention_only = FALSE OR needs_attention = TRUE)
            )
            SELECT
                c.container_status,
                COUNT(*) AS container_count
            FROM filtered_booking fb
            JOIN containers c ON fb.booking_no = c.booking_no
            GROUP BY c.container_status
            ORDER BY c.container_status;
        """)

        result = self.db.execute(query, {
            "office_code": office_code,
            "minutes": minutes,
            "booking_status": booking_status,
            "container_status": container_status,
            "include_attention_only": include_attention_only,
        })
        return [dict(row) for row in result.mappings().all()]

