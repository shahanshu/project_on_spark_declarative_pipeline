CREATE OR REFRESH MATERIALIZED VIEW sdp_project.gold.trips_golden (
  CONSTRAINT valid_city_id EXPECT (city_id IS NOT NULL),
  CONSTRAINT valid_business_date EXPECT (business_date IS NOT NULL)
)
COMMENT 'Gold layer view combining trips with city and calendar dimensions'
TBLPROPERTIES (
  'quality' = 'gold',
  'layer' = 'gold',
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact' = 'true'
)
AS
SELECT 
  t.trip_id,
  CAST(t.date AS DATE) AS business_date,
  t.city_id,
  c.city_name,
  t.passenger_type,
  t.distance_travelled_km,
  t.fare_amount,
  t.passenger_rating,
  t.driver_rating,
  cal.year,
  cal.month,
  cal.month_name,
  cal.quarter,
  cal.quarter_year,
  cal.day_of_week,
  cal.day_of_week_abbr,
  cal.is_weekday,
  cal.is_weekend,
  cal.is_holiday,
  cal.holiday_name,
  t.ingest_datatime AS bronze_ingest_timestamp,
  current_timestamp() AS gold_processed_timestamp
FROM sdp_project.silver.trips t
INNER JOIN sdp_project.silver.city c ON t.city_id = c.city_id
INNER JOIN sdp_project.silver.calendar cal ON CAST(t.date AS DATE) = cal.date
