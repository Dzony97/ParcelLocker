CREATE TABLE IF NOT EXISTS client (
    id_ BIGINT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(55) NOT NULL,
    last_name VARCHAR(55) NOT NULL,
    email VARCHAR(55) NOT NULL UNIQUE ,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    latitude float,
    longitude float
);

CREATE TABLE IF NOT EXISTS parcel_locker (
    id_ BIGINT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(55) NOT NULL,
    postal_code VARCHAR(6) NOT NULL,
    latitude float NOT NULL,
    longitude float NOT NULL
);

CREATE TABLE IF NOT EXISTS locker (
    id_ BIGINT AUTO_INCREMENT PRIMARY KEY,
    parcel_locker_id BIGINT NOT NULL,
    client_id BIGINT NULL DEFAULT NULL,
    package_id BIGINT NULL DEFAULT NULL,
    size VARCHAR(2),
    status VARCHAR(15) DEFAULT 'Available',
    FOREIGN KEY (parcel_locker_id) REFERENCES parcel_locker(id_) ON DELETE CASCADE,
    FOREIGN KEY (client_id) REFERENCES client(id_)
);

CREATE TABLE IF NOT EXISTS package (
    id_ BIGINT AUTO_INCREMENT PRIMARY KEY,
    sender_id BIGINT NOT NULL,
    receiver_id BIGINT NOT NULL,
    parcel_locker_id BIGINT NOT NULL,
    locker_id BIGINT NULL,
    size VARCHAR(2) NOT NULL,
    created_at DATETIME NOT NULL,
    delivered_at DATETIME NULL DEFAULT NULL,
    status VARCHAR(55),
    FOREIGN KEY (sender_id) REFERENCES client(id_),
    FOREIGN KEY (receiver_id) REFERENCES client(id_),
    FOREIGN KEY (parcel_locker_id) REFERENCES parcel_locker(id_),
    FOREIGN KEY (locker_id) REFERENCES locker(id_)
);

ALTER TABLE package
ADD FOREIGN KEY (locker_id) REFERENCES locker(id_);

ALTER TABLE locker
ADD FOREIGN KEY (package_id) REFERENCES package(id_);