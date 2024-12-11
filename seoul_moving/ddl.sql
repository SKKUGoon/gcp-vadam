-- Enable PostGIS extension if not already enabled
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create table: locations
CREATE TABLE nimbus.locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location_type VARCHAR NOT NULL,
    location_name VARCHAR NOT NULL,
    geometry GEOMETRY(POINT, 4326) NOT NULL
);

-- Create table: hjd
CREATE TABLE nimbus.hjd (
    sido_cd VARCHAR NOT NULL,
    sido_nm VARCHAR NOT NULL,
    sigungu_cd VARCHAR NOT NULL,
    sigungu_nm VARCHAR NOT NULL,
    adm_cd VARCHAR PRIMARY KEY,
    adm_nm VARCHAR NOT NULL,
    geometry GEOMETRY(POLYGON, 4326) NOT NULL
);

-- Allow MULTIPOLYGON in hjd.geometry
ALTER TABLE nimbus.hjd
    ALTER COLUMN geometry TYPE GEOMETRY(POLYGON, 4326)
    USING ST_SetSRID(ST_Multi(geometry), 4326);

-- Create table: sec
CREATE TABLE nimbus.sec (
    tot_reg_cd VARCHAR PRIMARY KEY,
    adm_nm VARCHAR NOT NULL,
    adm_cd VARCHAR NOT NULL,
    geometry GEOMETRY(POLYGON, 4326) NOT NULL,
    CONSTRAINT fk_hjd_adm_cd FOREIGN KEY (adm_cd) REFERENCES nimbus.hjd (adm_cd) ON DELETE CASCADE
);

-- Allow MULTIPOLYGON in sec.geometry
ALTER TABLE nimbus.sec
    ALTER COLUMN geometry TYPE GEOMETRY(POLYGON, 4326)
    USING ST_SetSRID(ST_Multi(geometry), 4326);

-- Create table: longterm_foreign
CREATE TABLE nimbus.longterm_foreign (
    date_str VARCHAR NOT NULL,
    hour INT NOT NULL,
    sec_code VARCHAR NOT NULL,
    total_population FLOAT4,
    chinese FLOAT4,
    non_chinese FLOAT4,
    CONSTRAINT fk_sec_code FOREIGN KEY (sec_code) REFERENCES nimbus.sec (tot_reg_cd) ON DELETE CASCADE
);

-- Drop any existing primary key if needed
ALTER TABLE nimbus.longterm_foreign DROP CONSTRAINT IF EXISTS longterm_foreign_pkey;

-- Add composite primary key
ALTER TABLE nimbus.longterm_foreign
ADD CONSTRAINT longterm_foreign_pkey PRIMARY KEY (date_str, hour, sec_code);

-- Create table: shortterm_foreign
CREATE TABLE nimbus.shortterm_foreign (
    date_str VARCHAR NOT NULL,
    hour INT NOT NULL,
    sec_code VARCHAR NOT NULL,
    total_population FLOAT4,
    chinese FLOAT4,
    non_chinese FLOAT4,
    CONSTRAINT fk_sec_code FOREIGN KEY (sec_code) REFERENCES nimbus.sec (tot_reg_cd) ON DELETE CASCADE
);

-- Drop any existing primary key if needed
ALTER TABLE nimbus.shortterm_foreign DROP CONSTRAINT IF EXISTS shortterm_foreign_pkey;

-- Add composite primary key
ALTER TABLE nimbus.shortterm_foreign
ADD CONSTRAINT shortterm_foreign_pkey PRIMARY KEY (date_str, hour, sec_code);

-- Create table: locals
CREATE TABLE nimbus.locals (
    date_str VARCHAR NOT NULL,
    hour INT NOT NULL,
    sec_code VARCHAR NOT NULL,
    total_population FLOAT4,
    male_00_09 FLOAT4,
    male_10_14 FLOAT4,
    male_15_19 FLOAT4,
    male_20_24 FLOAT4,
    male_25_29 FLOAT4,
    male_30_34 FLOAT4,
    male_35_39 FLOAT4,
    male_40_44 FLOAT4,
    male_45_49 FLOAT4,
    male_50_54 FLOAT4,
    male_55_59 FLOAT4,
    male_60_64 FLOAT4,
    male_65_69 FLOAT4,
    male_70_up FLOAT4,
    female_00_09 FLOAT4,
    female_10_14 FLOAT4,
    female_15_19 FLOAT4,
    female_20_24 FLOAT4,
    female_25_29 FLOAT4,
    female_30_34 FLOAT4,
    female_35_39 FLOAT4,
    female_40_44 FLOAT4,
    female_45_49 FLOAT4,
    female_50_54 FLOAT4,
    female_55_59 FLOAT4,
    female_60_64 FLOAT4,
    female_65_69 FLOAT4,
    female_70_up FLOAT4,
    CONSTRAINT fk_sec_code_locals FOREIGN KEY (sec_code) REFERENCES nimbus.sec (tot_reg_cd) ON DELETE CASCADE,
    CONSTRAINT locals_pkey PRIMARY KEY (date_str, hour, sec_code)
);