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
(1, NULL, 'S'), (1, NULL, 'S'), (1, NULL, 'M'), (1, NULL, 'M'), (1, NULL, 'L'), (1, NULL, 'L'),

(2, NULL, 'S'), (2, NULL, 'S'), (2, NULL, 'M'), (2, NULL, 'M'), (2, NULL, 'L'), (2, NULL, 'L'),

(3, NULL, 'S'), (3, NULL, 'S'), (3, NULL, 'M'), (3, NULL, 'M'), (3, NULL, 'L'), (3, NULL, 'L'),

(4, NULL, 'S'), (4, NULL, 'S'), (4, NULL, 'M'), (4, NULL, 'M'), (4, NULL, 'L'), (4, NULL, 'L');


