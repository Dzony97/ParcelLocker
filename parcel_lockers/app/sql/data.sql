INSERT INTO client (first_name, last_name, email, phone_number, latitude, longitude, user_id) VALUES
('John', 'Doe', 'john.doe@example.com', '1234567890', 37.7749, -122.4194, 1),
('Jane', 'Smith', 'jane.smith@example.com', '0987654321', 34.0522, -118.2437, 2),
('Alice', 'Johnson', 'alice.johnson@example.com', '5555555555', 40.7128, -74.0060, 3),
('Bob', 'Brown', 'bob.brown@example.com', '4444444444', 41.8781, -87.6298, 4);

INSERT INTO parcel_locker (city, postal_code, latitude, longitude) VALUES
('San Francisco', '94103', 37.7749, -122.4194),
('Los Angeles', '90001', 34.0522, -118.2437),
('New York', '10001', 40.7128, -74.0060),
('Chicago', '60601', 41.8781, -87.6298);

INSERT INTO locker (parcel_locker_id, client_id, size, status) VALUES
(1, NULL, 'S', 'Available'), (1, NULL, 'S', 'Available'), (1, NULL, 'M', 'Available'), (1, NULL, 'M', 'Available'), (1, NULL, 'L', 'Available'), (1, NULL, 'L', 'Available'),

(2, NULL, 'S', 'Available'), (2, NULL, 'S', 'Available'), (2, NULL, 'M', 'Available'), (2, NULL, 'M', 'Available'), (2, NULL, 'L', 'Available'), (2, NULL, 'L', 'Available'),

(3, NULL, 'S', 'Available'), (3, NULL, 'S', 'Available'), (3, NULL, 'M', 'Available'), (3, NULL, 'M', 'Available'), (3, NULL, 'L', 'Available'), (3, NULL, 'L', 'Available'),

(4, NULL, 'S', 'Available'), (4, NULL, 'S', 'Available'), (4, NULL, 'M', 'Available'), (4, NULL, 'M', 'Available'), (4, NULL, 'L', 'Available'), (4, NULL, 'L', 'Available');


