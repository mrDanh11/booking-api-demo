-- Seed data for Shipping Booking Information API
-- Safe to run on a fresh database

BEGIN;

-- Clear old data
TRUNCATE TABLE containers, bookings, voyages, vessels RESTART IDENTITY CASCADE;

-- Vessels
INSERT INTO vessels (vessel_code, vessel_name) VALUES ('ONEAL', 'ONE ALTAIR');
INSERT INTO vessels (vessel_code, vessel_name) VALUES ('EVRGR', 'EVER GREEN');
INSERT INTO vessels (vessel_code, vessel_name) VALUES ('MSCMY', 'MSC MAYA');
INSERT INTO vessels (vessel_code, vessel_name) VALUES ('MAERS', 'MAERSK HANOI');
INSERT INTO vessels (vessel_code, vessel_name) VALUES ('COSCO', 'COSCO STAR');
INSERT INTO vessels (vessel_code, vessel_name) VALUES ('HMMBL', 'HMM BLUE OCEAN');

-- Voyages
INSERT INTO voyages (vessel_id, voyage_no, origin_port, destination_port, etd, eta) VALUES (1, '001E', 'VNHPH', 'NLRTM', '2026-07-01 08:00:00', '2026-07-14 08:00:00');
INSERT INTO voyages (vessel_id, voyage_no, origin_port, destination_port, etd, eta) VALUES (1, '002W', 'THBKK', 'DEHAM', '2026-07-10 08:00:00', '2026-07-24 08:00:00');
INSERT INTO voyages (vessel_id, voyage_no, origin_port, destination_port, etd, eta) VALUES (2, '001E', 'THBKK', 'JPTYO', '2026-07-05 08:00:00', '2026-07-19 08:00:00');
INSERT INTO voyages (vessel_id, voyage_no, origin_port, destination_port, etd, eta) VALUES (2, '002W', 'SGSIN', 'CNSHA', '2026-07-14 08:00:00', '2026-07-29 08:00:00');
INSERT INTO voyages (vessel_id, voyage_no, origin_port, destination_port, etd, eta) VALUES (3, '001E', 'SGSIN', 'USLAX', '2026-07-09 08:00:00', '2026-07-24 08:00:00');
INSERT INTO voyages (vessel_id, voyage_no, origin_port, destination_port, etd, eta) VALUES (3, '002W', 'MYPKG', 'USNYC', '2026-07-18 08:00:00', '2026-08-03 08:00:00');
INSERT INTO voyages (vessel_id, voyage_no, origin_port, destination_port, etd, eta) VALUES (4, '001E', 'MYPKG', 'NLRTM', '2026-07-13 08:00:00', '2026-07-29 08:00:00');
INSERT INTO voyages (vessel_id, voyage_no, origin_port, destination_port, etd, eta) VALUES (4, '002W', 'VNSGN', 'DEHAM', '2026-07-22 08:00:00', '2026-08-08 08:00:00');
INSERT INTO voyages (vessel_id, voyage_no, origin_port, destination_port, etd, eta) VALUES (5, '001E', 'VNSGN', 'JPTYO', '2026-07-17 08:00:00', '2026-08-03 08:00:00');
INSERT INTO voyages (vessel_id, voyage_no, origin_port, destination_port, etd, eta) VALUES (5, '002W', 'VNHPH', 'CNSHA', '2026-07-26 08:00:00', '2026-08-13 08:00:00');
INSERT INTO voyages (vessel_id, voyage_no, origin_port, destination_port, etd, eta) VALUES (6, '001E', 'VNHPH', 'USLAX', '2026-07-21 08:00:00', '2026-08-08 08:00:00');
INSERT INTO voyages (vessel_id, voyage_no, origin_port, destination_port, etd, eta) VALUES (6, '002W', 'THBKK', 'USNYC', '2026-07-30 08:00:00', '2026-08-18 08:00:00');

-- Bookings
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000001', 'ABC LOGISTICS', 1, 'CANCELLED', 'FOOTWEAR', '2026-07-02 08:00:00', '2026-07-02 09:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000002', 'PACIFIC FREIGHT', 2, 'CONFIRMED', 'FROZEN SEAFOOD', '2026-07-03 08:00:00', '2026-07-03 10:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000003', 'GLOBAL OCEAN', 3, 'PENDING', 'PLASTIC RESIN', '2026-07-04 08:00:00', '2026-07-04 11:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000004', 'SUNRISE SHIPPING', 4, 'DRAFT', 'ELECTRONICS', '2026-07-05 08:00:00', '2026-07-05 12:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000005', 'MEKONG CARGO', 5, 'CANCELLED', 'GARMENT', '2026-07-06 08:00:00', '2026-07-06 13:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000006', 'BLUE SEA LOGISTICS', 6, 'CONFIRMED', 'MACHINERY PARTS', '2026-07-07 08:00:00', '2026-07-07 14:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000007', 'STARLINK FORWARDING', 7, 'PENDING', 'FURNITURE', '2026-07-08 08:00:00', '2026-07-08 15:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000008', 'LOTUS TRANSPORT', 8, 'DRAFT', 'GENERAL CARGO', '2026-07-09 08:00:00', '2026-07-09 16:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000009', 'EASTERN FREIGHT', 9, 'CANCELLED', 'FOOTWEAR', '2026-07-10 08:00:00', '2026-07-10 17:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000010', 'TRANSWORLD LOGISTICS', 10, 'CONFIRMED', 'FROZEN SEAFOOD', '2026-07-11 08:00:00', '2026-07-11 18:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000011', 'VIET CARGO EXPRESS', 11, 'PENDING', 'PLASTIC RESIN', '2026-07-12 08:00:00', '2026-07-12 19:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000012', 'HORIZON SUPPLY CHAIN', 12, 'DRAFT', 'ELECTRONICS', '2026-07-13 08:00:00', '2026-07-13 20:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000013', 'ABC LOGISTICS', 1, 'CANCELLED', 'GARMENT', '2026-07-14 08:00:00', '2026-07-14 21:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000014', 'PACIFIC FREIGHT', 2, 'CONFIRMED', 'MACHINERY PARTS', '2026-07-15 08:00:00', '2026-07-15 22:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000015', 'GLOBAL OCEAN', 3, 'PENDING', 'FURNITURE', '2026-07-16 08:00:00', '2026-07-16 23:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000016', 'SUNRISE SHIPPING', 4, 'DRAFT', 'GENERAL CARGO', '2026-07-17 08:00:00', '2026-07-18 00:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000017', 'MEKONG CARGO', 5, 'CANCELLED', 'FOOTWEAR', '2026-07-18 08:00:00', '2026-07-19 01:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000018', 'BLUE SEA LOGISTICS', 6, 'CONFIRMED', 'FROZEN SEAFOOD', '2026-07-19 08:00:00', '2026-07-20 02:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000019', 'STARLINK FORWARDING', 7, 'PENDING', 'PLASTIC RESIN', '2026-07-20 08:00:00', '2026-07-21 03:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000020', 'LOTUS TRANSPORT', 8, 'DRAFT', 'ELECTRONICS', '2026-07-21 08:00:00', '2026-07-22 04:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000021', 'EASTERN FREIGHT', 9, 'CANCELLED', 'GARMENT', '2026-07-22 08:00:00', '2026-07-23 05:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000022', 'TRANSWORLD LOGISTICS', 10, 'CONFIRMED', 'MACHINERY PARTS', '2026-07-23 08:00:00', '2026-07-24 06:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000023', 'VIET CARGO EXPRESS', 11, 'PENDING', 'FURNITURE', '2026-07-24 08:00:00', '2026-07-25 07:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000024', 'HORIZON SUPPLY CHAIN', 12, 'DRAFT', 'GENERAL CARGO', '2026-07-25 08:00:00', '2026-07-26 08:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000025', 'ABC LOGISTICS', 1, 'CANCELLED', 'FOOTWEAR', '2026-07-26 08:00:00', '2026-07-27 09:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000026', 'PACIFIC FREIGHT', 2, 'CONFIRMED', 'FROZEN SEAFOOD', '2026-07-27 08:00:00', '2026-07-28 10:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000027', 'GLOBAL OCEAN', 3, 'PENDING', 'PLASTIC RESIN', '2026-07-28 08:00:00', '2026-07-29 11:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000028', 'SUNRISE SHIPPING', 4, 'DRAFT', 'ELECTRONICS', '2026-07-29 08:00:00', '2026-07-30 12:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000029', 'MEKONG CARGO', 5, 'CANCELLED', 'GARMENT', '2026-07-30 08:00:00', '2026-07-31 13:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000030', 'BLUE SEA LOGISTICS', 6, 'CONFIRMED', 'MACHINERY PARTS', '2026-07-31 08:00:00', '2026-08-01 14:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000031', 'STARLINK FORWARDING', 7, 'PENDING', 'FURNITURE', '2026-08-01 08:00:00', '2026-08-02 15:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000032', 'LOTUS TRANSPORT', 8, 'DRAFT', 'GENERAL CARGO', '2026-08-02 08:00:00', '2026-08-03 16:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000033', 'EASTERN FREIGHT', 9, 'CANCELLED', 'FOOTWEAR', '2026-08-03 08:00:00', '2026-08-04 17:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000034', 'TRANSWORLD LOGISTICS', 10, 'CONFIRMED', 'FROZEN SEAFOOD', '2026-08-04 08:00:00', '2026-08-05 18:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000035', 'VIET CARGO EXPRESS', 11, 'PENDING', 'PLASTIC RESIN', '2026-08-05 08:00:00', '2026-08-06 19:00:00');
INSERT INTO bookings (booking_no, customer_name, voyage_id, booking_status, cargo_description, created_at, updated_at) VALUES ('BKG0000036', 'HORIZON SUPPLY CHAIN', 12, 'DRAFT', 'ELECTRONICS', '2026-08-06 08:00:00', '2026-08-07 20:00:00');

-- Containers
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234501', 'BKG0000001', '40HC', 'SL00101', 15850.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234502', 'BKG0000001', '40GP', 'SL00102', 15975.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234503', 'BKG0000002', '40GP', 'SL00201', 16200.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234504', 'BKG0000002', '45HC', 'SL00202', 16325.00, 'EMPTY');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234505', 'BKG0000002', '20GP', 'SL00203', 16450.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234506', 'BKG0000003', '45HC', 'SL00301', 16550.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234507', 'BKG0000004', '20GP', 'SL00401', 16900.00, 'EMPTY');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234508', 'BKG0000004', '40HC', 'SL00402', 17025.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234509', 'BKG0000005', '40HC', 'SL00501', 17250.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234510', 'BKG0000005', '40GP', 'SL00502', 17375.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234511', 'BKG0000005', '45HC', 'SL00503', 17500.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234512', 'BKG0000006', '40GP', 'SL00601', 17600.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234513', 'BKG0000007', '45HC', 'SL00701', 17950.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234514', 'BKG0000007', '20GP', 'SL00702', 18075.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234515', 'BKG0000008', '20GP', 'SL00801', 18300.00, 'EMPTY');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234516', 'BKG0000008', '40HC', 'SL00802', 18425.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234517', 'BKG0000008', '40GP', 'SL00803', 18550.00, 'EMPTY');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234518', 'BKG0000009', '40HC', 'SL00901', 18650.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234519', 'BKG0000010', '40GP', 'SL01001', 19000.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234520', 'BKG0000010', '45HC', 'SL01002', 19125.00, 'EMPTY');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234521', 'BKG0000011', '45HC', 'SL01101', 19350.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234522', 'BKG0000011', '20GP', 'SL01102', 19475.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234523', 'BKG0000011', '40HC', 'SL01103', 19600.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234524', 'BKG0000012', '20GP', 'SL01201', 19700.00, 'EMPTY');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234525', 'BKG0000013', '40HC', 'SL01301', 20050.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234526', 'BKG0000013', '40GP', 'SL01302', 20175.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234527', 'BKG0000014', '40GP', 'SL01401', 20400.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234528', 'BKG0000014', '45HC', 'SL01402', 20525.00, 'EMPTY');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234529', 'BKG0000014', '20GP', 'SL01403', 20650.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234530', 'BKG0000015', '45HC', 'SL01501', 20750.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234531', 'BKG0000016', '20GP', 'SL01601', 21100.00, 'EMPTY');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234532', 'BKG0000016', '40HC', 'SL01602', 21225.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234533', 'BKG0000017', '40HC', 'SL01701', 21450.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234534', 'BKG0000017', '40GP', 'SL01702', 21575.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234535', 'BKG0000017', '45HC', 'SL01703', 21700.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234536', 'BKG0000018', '40GP', 'SL01801', 21800.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234537', 'BKG0000019', '45HC', 'SL01901', 22150.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234538', 'BKG0000019', '20GP', 'SL01902', 22275.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234539', 'BKG0000020', '20GP', 'SL02001', 22500.00, 'EMPTY');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234540', 'BKG0000020', '40HC', 'SL02002', 22625.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234541', 'BKG0000020', '40GP', 'SL02003', 22750.00, 'EMPTY');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234542', 'BKG0000021', '40HC', 'SL02101', 22850.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234543', 'BKG0000022', '40GP', 'SL02201', 23200.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234544', 'BKG0000022', '45HC', 'SL02202', 23325.00, 'EMPTY');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234545', 'BKG0000023', '45HC', 'SL02301', 23550.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234546', 'BKG0000023', '20GP', 'SL02302', 23675.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234547', 'BKG0000023', '40HC', 'SL02303', 23800.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234548', 'BKG0000024', '20GP', 'SL02401', 23900.00, 'EMPTY');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234549', 'BKG0000025', '40HC', 'SL02501', 24250.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234550', 'BKG0000025', '40GP', 'SL02502', 24375.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234551', 'BKG0000026', '40GP', 'SL02601', 24600.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234552', 'BKG0000026', '45HC', 'SL02602', 24725.00, 'EMPTY');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234553', 'BKG0000026', '20GP', 'SL02603', 24850.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234554', 'BKG0000027', '45HC', 'SL02701', 24950.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234555', 'BKG0000028', '20GP', 'SL02801', 25300.00, 'EMPTY');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234556', 'BKG0000028', '40HC', 'SL02802', 25425.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234557', 'BKG0000029', '40HC', 'SL02901', 25650.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234558', 'BKG0000029', '40GP', 'SL02902', 25775.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234559', 'BKG0000029', '45HC', 'SL02903', 25900.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234560', 'BKG0000030', '40GP', 'SL03001', 26000.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234561', 'BKG0000031', '45HC', 'SL03101', 26350.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234562', 'BKG0000031', '20GP', 'SL03102', 26475.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234563', 'BKG0000032', '20GP', 'SL03201', 26700.00, 'EMPTY');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234564', 'BKG0000032', '40HC', 'SL03202', 26825.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234565', 'BKG0000032', '40GP', 'SL03203', 26950.00, 'EMPTY');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234566', 'BKG0000033', '40HC', 'SL03301', 27050.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234567', 'BKG0000034', '40GP', 'SL03401', 27400.00, 'GATED_IN');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234568', 'BKG0000034', '45HC', 'SL03402', 27525.00, 'EMPTY');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234569', 'BKG0000035', '45HC', 'SL03501', 27750.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234570', 'BKG0000035', '20GP', 'SL03502', 27875.00, 'STUFFED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234571', 'BKG0000035', '40HC', 'SL03503', 28000.00, 'LOADED');
INSERT INTO containers (container_no, booking_no, container_type, seal_no, gross_weight, container_status) VALUES ('ONEU1234572', 'BKG0000036', '20GP', 'SL03601', 28100.00, 'EMPTY');

COMMIT;