CREATE OR REFRESH MATERIALIZED VIEW sdp_project.gold.trips_visakhapatnam
AS (
SELECT *
FROM sdp_project.gold.trips_golden
WHERE city_id = 'AP01'
);