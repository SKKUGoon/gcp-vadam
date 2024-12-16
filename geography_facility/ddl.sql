-- Create table: locations
CREATE TABLE nimbus.locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_type VARCHAR NOT NULL,
    location_name VARCHAR NOT NULL,
    address VARCHAR,
    geometry GEOMETRY(POINT, 4326) NOT NULL
);