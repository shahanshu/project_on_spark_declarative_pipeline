CREATE OR REFRESH MATERIALIZED VIEW sdp_project.gold.trips_coimbatore
AS (
SELECT *
FROM sdp_project.gold.trips_golden
WHERE city_id = 'TN01'
);