INSERT INTO client (first_name, last_name, email, phone_number, latitude, longitude) VALUES
('John', 'Doe', 'john.doe@example.com', '1234567890', 37.7749, -122.4194),
('Jane', 'Smith', 'jane.smith@example.com', '0987654321', 34.0522, -118.2437),
('Alice', 'Johnson', 'alice.johnson@example.com', '5555555555', 40.7128, -74.0060),
('Bob', 'Brown', 'bob.brown@example.com', '4444444444', 41.8781, -87.6298);

INSERT INTO parcel_locker (city, postal_code, latitude, longitude, available_slots) VALUES
('San Francisco', '94103', 37.7749, -122.4194, 10),
('Los Angeles', '90001', 34.0522, -118.2437, 5),
('New York', '10001', 40.7128, -74.0060, 8),
('Chicago', '60601', 41.8781, -87.6298, 12);

INSERT INTO locker (parcel_locker_id, client_id, size) VALUES
(1, 1, 'M'),  -- Locker in San Francisco for John Doe
(1, 2, 'S'),  -- Locker in San Francisco for Jane Smith
(2, 3, 'L'),  -- Locker in Los Angeles for Alice Johnson
(3, 4, 'M'),  -- Locker in New York for Bob Brown
(2, NULL, 'S');  -- Locker in Los Angeles, available (not assigned to any client)

INSERT INTO package (sender_id, receiver_id, parcel_locker_id, locker_id, size, created_at, status) VALUES
(1, 2, 1, 1, 'M', NOW(), 'Pending'),  -- Package from John to Jane in SF
(3, 4, 3, 3, 'L', NOW(), 'Delivered'),  -- Package from Alice to Bob in NY
(2, 1, 2, 2, 'S', NOW(), 'Pending');  -- Package from Jane to John in LA
