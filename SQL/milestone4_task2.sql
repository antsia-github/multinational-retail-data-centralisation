-------Task 2: Locations with the highest number of stores---------
SELECT locality, COUNT(locality) as total_no_stores
FROM dim_store_details
GROUP BY locality
ORDER BY total_no_stores DESC 
LIMIT 7;