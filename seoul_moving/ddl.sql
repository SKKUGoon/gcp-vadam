-- Enable PostGIS extension if not already enabled
CREATE EXTENSION IF NOT EXISTS postgis;

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
    total_population FLOAT NOT NULL,
    chinese FLOAT NOT NULL,
    non_chinese FLOAT NOT NULL,
    CONSTRAINT fk_sec_code FOREIGN KEY (sec_code) REFERENCES nimbus.sec (tot_reg_cd) ON DELETE CASCADE
);

-- Drop any existing primary key if needed
ALTER TABLE nimbus.longterm_foreign DROP CONSTRAINT IF EXISTS longterm_foreign_pkey;

-- Add composite primary key
ALTER TABLE nimbus.longterm_foreign
ADD CONSTRAINT longterm_foreign_pkey PRIMARY KEY (date_str, hour, sec_code);

-- Create table: locals
CREATE TABLE nimbus.locals (
    date_str VARCHAR NOT NULL,
    hour INT NOT NULL,
    sec_code VARCHAR NOT NULL,
    total_population FLOAT NOT NULL,
    male_00_09 FLOAT NOT NULL,
    male_10_14 FLOAT NOT NULL,
    male_15_19 FLOAT NOT NULL,
    male_20_24 FLOAT NOT NULL,
    male_25_29 FLOAT NOT NULL,
    male_30_34 FLOAT NOT NULL,
    male_35_39 FLOAT NOT NULL,
    male_40_44 FLOAT NOT NULL,
    male_45_49 FLOAT NOT NULL,
    male_50_54 FLOAT NOT NULL,
    male_55_59 FLOAT NOT NULL,
    male_60_64 FLOAT NOT NULL,
    male_65_69 FLOAT NOT NULL,
    male_70_up FLOAT NOT NULL,
    female_00_09 FLOAT NOT NULL,
    female_10_14 FLOAT NOT NULL,
    female_15_19 FLOAT NOT NULL,
    female_20_24 FLOAT NOT NULL,
    female_25_29 FLOAT NOT NULL,
    female_30_34 FLOAT NOT NULL,
    female_35_39 FLOAT NOT NULL,
    female_40_44 FLOAT NOT NULL,
    female_45_49 FLOAT NOT NULL,
    female_50_54 FLOAT NOT NULL,
    female_55_59 FLOAT NOT NULL,
    female_60_64 FLOAT NOT NULL,
    female_65_69 FLOAT NOT NULL,
    female_70_up FLOAT NOT NULL,
    CONSTRAINT fk_sec_code_locals FOREIGN KEY (sec_code) REFERENCES nimbus.sec (tot_reg_cd) ON DELETE CASCADE,
    CONSTRAINT locals_pkey PRIMARY KEY (date_str, hour, sec_code)
);