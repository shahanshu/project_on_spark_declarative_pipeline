CREATE OR REFRESH MATERIALIZED VIEW sdp_project.gold.trips_kochi
AS (
SELECT *
FROM sdp_project.gold.trips_golden
WHERE city_id = 'KL01'
);