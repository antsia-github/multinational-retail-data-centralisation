----------Task 1: Number of stores in top 3 countries ---------
SELECT country_code AS country, COUNT(country_code) as total_no_stores
FROM dim_store_details
GROUP BY country_code
ORDER BY total_no_stores DESC 
LIMIT 3;
