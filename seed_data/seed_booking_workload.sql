-- Seed data for Practice 2: Office / Booking Workload Summary
-- Safe to re-run: only touches `offices` plus a dedicated set of rows
-- prefixed with BKGW / WKL so it never collides with seed_booking_api.sql

BEGIN;

INSERT INTO offices (office_code, office_name, country_code) VALUES
    ('RICHQ', 'Richmond Operation Office', 'US'),
    ('SINBB', 'Singapore Booking Office', 'SG'),
    ('SGNBB', 'Saigon Booking Office', 'VN')
ON CONFLICT (office_code) DO NOTHING;

-- Clean up rows from a previous run of this script only
DELETE FROM containers WHERE booking_no LIKE 'BKGW%';
DELETE FROM bookings WHERE booking_no LIKE 'BKGW%';
DELETE FROM voyages WHERE voyage_no LIKE 'WKL%';
DELETE FROM vessels WHERE vessel_code IN ('WKLD1', 'WKLD2', 'WKLD3');

INSERT INTO vessels (vessel_code, vessel_name) VALUES
    ('WKLD1', 'WORKLOAD EXPRESS'),
    ('WKLD2', 'WORKLOAD PIONEER'),
    ('WKLD3', 'WORKLOAD HORIZON');

INSERT INTO voyages (vessel_id, voyage_no, origin_port, destination_port) VALUES
    ((SELECT vessel_id FROM vessels WHERE vessel_code = 'WKLD1'), 'WKL01', 'VNSGN', 'USLAX'),
    ((SELECT vessel_id FROM vessels WHERE vessel_code = 'WKLD1'), 'WKL02', 'VNSGN', 'JPNGO'),
    ((SELECT vessel_id FROM vessels WHERE vessel_code = 'WKLD1'), 'WKL03', 'CNSHA', 'USLAX'),
    ((SELECT vessel_id FROM vessels WHERE vessel_code = 'WKLD2'), 'WKL04', 'VNHPH', 'NLRTM'),
    ((SELECT vessel_id FROM vessels WHERE vessel_code = 'WKLD2'), 'WKL05', 'THBKK', 'DEHAM'),
    ((SELECT vessel_id FROM vessels WHERE vessel_code = 'WKLD3'), 'WKL06', 'SGSIN', 'CNSHA'),
    ((SELECT vessel_id FROM vessels WHERE vessel_code = 'WKLD3'), 'WKL07', 'MYPKG', 'USNYC'),
    ((SELECT vessel_id FROM vessels WHERE vessel_code = 'WKLD3'), 'WKL08', 'VNSGN', 'DEHAM'),
    ((SELECT vessel_id FROM vessels WHERE vessel_code = 'WKLD3'), 'WKL09', 'VNHPH', 'JPTYO');

-- Bookings: cover every operation_status, every office, every container_status
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, handling_office, created_at, updated_at) VALUES
    -- READY: CONFIRMED with containers -> needs_attention = false
    ('BKGW00001', 'ABC LOGISTICS',
        (SELECT voyage_id FROM voyages WHERE voyage_no = 'WKL01'),
        'CONFIRMED', 'RICHQ',
        CURRENT_TIMESTAMP - INTERVAL '60 minutes', CURRENT_TIMESTAMP - INTERVAL '30 minutes'),

    -- PENDING, no containers -> needs_attention = true (PENDING rule)
    ('BKGW00002', 'GLOBAL FREIGHT',
        (SELECT voyage_id FROM voyages WHERE voyage_no = 'WKL02'),
        'PENDING', 'RICHQ',
        CURRENT_TIMESTAMP - INTERVAL '90 minutes', CURRENT_TIMESTAMP - INTERVAL '45 minutes'),

    -- NEEDS_CONTAINER: CONFIRMED, zero containers -> needs_attention = true
    ('BKGW00003', 'NO CONTAINER CUSTOMER',
        (SELECT voyage_id FROM voyages WHERE voyage_no = 'WKL03'),
        'CONFIRMED', 'RICHQ',
        CURRENT_TIMESTAMP - INTERVAL '120 minutes', CURRENT_TIMESTAMP - INTERVAL '50 minutes'),

    -- Different office (SINBB) -> must never show up when querying RICHQ
    ('BKGW00004', 'OTHER OFFICE CUSTOMER',
        (SELECT voyage_id FROM voyages WHERE voyage_no = 'WKL01'),
        'CONFIRMED', 'SINBB',
        CURRENT_TIMESTAMP - INTERVAL '60 minutes', CURRENT_TIMESTAMP - INTERVAL '30 minutes'),

    -- COMPLETED, updated 2000 minutes ago -> excluded by default minutes=1440,
    -- only shows up when caller passes ?minutes=3000 or higher
    ('BKGW00005', 'DONE DEAL LTD',
        (SELECT voyage_id FROM voyages WHERE voyage_no = 'WKL02'),
        'COMPLETED', 'RICHQ',
        CURRENT_TIMESTAMP - INTERVAL '2000 minutes', CURRENT_TIMESTAMP - INTERVAL '2000 minutes'),

    -- CANCELLED, also outside the default lookback window
    ('BKGW00006', 'CANCELLED CO',
        (SELECT voyage_id FROM voyages WHERE voyage_no = 'WKL03'),
        'CANCELLED', 'RICHQ',
        CURRENT_TIMESTAMP - INTERVAL '3000 minutes', CURRENT_TIMESTAMP - INTERVAL '3000 minutes'),

    -- All 3 containers DISCHARGED -> test ?container_status=DISCHARGED
    ('BKGW00007', 'DISCHARGE PORT LOGISTICS',
        (SELECT voyage_id FROM voyages WHERE voyage_no = 'WKL04'),
        'CONFIRMED', 'RICHQ',
        CURRENT_TIMESTAMP - INTERVAL '80 minutes', CURRENT_TIMESTAMP - INTERVAL '20 minutes'),

    -- One DELIVERED container -> test ?container_status=DELIVERED
    ('BKGW00008', 'FINAL MILE CARGO',
        (SELECT voyage_id FROM voyages WHERE voyage_no = 'WKL05'),
        'CONFIRMED', 'RICHQ',
        CURRENT_TIMESTAMP - INTERVAL '100 minutes', CURRENT_TIMESTAMP - INTERVAL '10 minutes'),

    -- PENDING at a different office, has an EMPTY container
    ('BKGW00009', 'SINGAPORE TRADERS',
        (SELECT voyage_id FROM voyages WHERE voyage_no = 'WKL04'),
        'PENDING', 'SINBB',
        CURRENT_TIMESTAMP - INTERVAL '70 minutes', CURRENT_TIMESTAMP - INTERVAL '15 minutes'),

    -- Third office (SGNBB), CONFIRMED with containers
    ('BKGW00010', 'SAIGON EXPORTERS',
        (SELECT voyage_id FROM voyages WHERE voyage_no = 'WKL06'),
        'CONFIRMED', 'SGNBB',
        CURRENT_TIMESTAMP - INTERVAL '40 minutes', CURRENT_TIMESTAMP - INTERVAL '5 minutes'),

    -- SGNBB, COMPLETED
    ('BKGW00011', 'MEKONG DELTA TRADING',
        (SELECT voyage_id FROM voyages WHERE voyage_no = 'WKL07'),
        'COMPLETED', 'SGNBB',
        CURRENT_TIMESTAMP - INTERVAL '200 minutes', CURRENT_TIMESTAMP - INTERVAL '150 minutes'),

    -- SGNBB, CANCELLED
    ('BKGW00012', 'HO CHI MINH FORWARDING',
        (SELECT voyage_id FROM voyages WHERE voyage_no = 'WKL08'),
        'CANCELLED', 'SGNBB',
        CURRENT_TIMESTAMP - INTERVAL '300 minutes', CURRENT_TIMESTAMP - INTERVAL '250 minutes'),

    -- 5 containers, one of every status -> broadest container_status_summary coverage
    ('BKGW00013', 'FULL SPECTRUM SHIPPING',
        (SELECT voyage_id FROM voyages WHERE voyage_no = 'WKL09'),
        'CONFIRMED', 'RICHQ',
        CURRENT_TIMESTAMP - INTERVAL '110 minutes', CURRENT_TIMESTAMP - INTERVAL '5 minutes'),

    -- PENDING but already has containers -> still needs_attention = true (PENDING rule wins)
    ('BKGW00014', 'ALREADY PACKED CO',
        (SELECT voyage_id FROM voyages WHERE voyage_no = 'WKL01'),
        'PENDING', 'RICHQ',
        CURRENT_TIMESTAMP - INTERVAL '30 minutes', CURRENT_TIMESTAMP - INTERVAL '2 minutes'),

    -- Another NEEDS_CONTAINER case, for pagination/volume testing
    ('BKGW00015', 'LAST MINUTE BOOKING',
        (SELECT voyage_id FROM voyages WHERE voyage_no = 'WKL02'),
        'CONFIRMED', 'RICHQ',
        CURRENT_TIMESTAMP - INTERVAL '15 minutes', CURRENT_TIMESTAMP - INTERVAL '1 minutes');

INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES
    ('WKLU0000001', 'BKGW00001', '40HC', 'SLW00001', 25000.50, 'LOADED'),
    ('WKLU0000002', 'BKGW00001', '20GP', 'SLW00002', 18000.00, 'GATE_IN'),

    ('WKLU0000003', 'BKGW00005', '40GP', 'SLW00003', 21000.00, 'DELIVERED'),

    ('WKLU0000004', 'BKGW00006', '20GP', 'SLW00004', 17000.00, 'DISCHARGED'),

    ('WKLU0000005', 'BKGW00007', '40HC', 'SLW00005', 24000.00, 'DISCHARGED'),
    ('WKLU0000006', 'BKGW00007', '40GP', 'SLW00006', 23500.00, 'DISCHARGED'),
    ('WKLU0000007', 'BKGW00007', '20GP', 'SLW00007', 16000.00, 'DISCHARGED'),

    ('WKLU0000008', 'BKGW00008', '45HC', 'SLW00008', 27000.00, 'DELIVERED'),

    ('WKLU0000009', 'BKGW00009', '20GP', 'SLW00009', 15500.00, 'EMPTY'),

    ('WKLU0000010', 'BKGW00010', '40HC', 'SLW00010', 26000.00, 'LOADED'),
    ('WKLU0000011', 'BKGW00010', '20GP', 'SLW00011', 15000.00, 'EMPTY'),

    ('WKLU0000012', 'BKGW00013', '20GP', 'SLW00012', 15200.00, 'EMPTY'),
    ('WKLU0000013', 'BKGW00013', '40GP', 'SLW00013', 19800.00, 'GATE_IN'),
    ('WKLU0000014', 'BKGW00013', '40HC', 'SLW00014', 24500.00, 'LOADED'),
    ('WKLU0000015', 'BKGW00013', '45HC', 'SLW00015', 27500.00, 'DISCHARGED'),
    ('WKLU0000016', 'BKGW00013', '20GP', 'SLW00016', 14800.00, 'DELIVERED'),

    ('WKLU0000017', 'BKGW00014', '40GP', 'SLW00017', 20000.00, 'GATE_IN'),
    ('WKLU0000018', 'BKGW00014', '40HC', 'SLW00018', 23000.00, 'LOADED');

COMMIT;
