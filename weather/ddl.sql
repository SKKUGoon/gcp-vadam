-- Create the 'station' table
CREATE TABLE lake.station (
    stn_id VARCHAR(255) NOT NULL PRIMARY KEY,
    lng FLOAT,
    lat FLOAT,
    stn_cd1 VARCHAR(255),
    ht FLOAT,
    ht_pa FLOAT,
    ht_ta FLOAT,
    st_wd FLOAT,
    st_rn FLOAT,
    stn_cd2 VARCHAR(255),
    stn_nm_kor VARCHAR(255),
    stn_nm_eng VARCHAR(255),
    fct_cd VARCHAR(255),
    pnu_bjd VARCHAR(255),
    updated_date DATE,
    is_deleted BOOLEAN
);

-- Create the 'measurements' table
CREATE TABLE lake.measurements_day (
    datetime_str VARCHAR(255),
    stn_id VARCHAR(255),
    wind_direction FLOAT,
    wind_speed FLOAT,
    gust_direction FLOAT,
    gust_speed FLOAT,
    gust_time VARCHAR(255),
    ground_hpa FLOAT,
    sealevel_hpa FLOAT,
    temperature FLOAT,
    humidity FLOAT,
    rain FLOAT,
    rain_day1 FLOAT,
    rain_day2 FLOAT,
    rain_strength FLOAT,
    snow_3hours FLOAT,
    snow_day FLOAT,
    snow_cumul FLOAT,
    weather_report VARCHAR(255),
    cloud_total FLOAT,
    cloud_mid_ht FLOAT,
    cloud_min_ht FLOAT,
    cloud_type VARCHAR(255),
    visibility FLOAT,
    sun VARCHAR(255),
    status_ground VARCHAR(255),
    temperature_ground FLOAT,
    status_sealevel VARCHAR(255),
    wave FLOAT,
    is_raining VARCHAR(255),
    PRIMARY KEY (datetime_str, stn_id),
    FOREIGN KEY (stn_id) REFERENCES lake.station(stn_id)
);

-- Create the 'measurements' table
CREATE TABLE lake.measurements_time (
    datetime_str VARCHAR(255),
    stn_id VARCHAR(255),
    wind_direction FLOAT,
    wind_speed FLOAT,
    gust_direction FLOAT,
    gust_speed FLOAT,
    gust_time VARCHAR(255),
    ground_hpa FLOAT,
    sealevel_hpa FLOAT,
    temperature FLOAT,
    humidity FLOAT,
    rain FLOAT,
    rain_day1 FLOAT,
    rain_day2 FLOAT,
    rain_strength FLOAT,
    snow_3hours FLOAT,
    snow_day FLOAT,
    snow_cumul FLOAT,
    weather_report VARCHAR(255),
    cloud_total FLOAT,
    cloud_mid_ht FLOAT,
    cloud_min_ht FLOAT,
    cloud_type VARCHAR(255),
    visibility FLOAT,
    sun VARCHAR(255),
    status_ground VARCHAR(255),
    temperature_ground FLOAT,
    status_sealevel VARCHAR(255),
    wave FLOAT,
    is_raining VARCHAR(255),
    PRIMARY KEY (datetime_str, stn_id),
    FOREIGN KEY (stn_id) REFERENCES lake.station(stn_id)
);