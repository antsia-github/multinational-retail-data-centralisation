---Task 4---
SELECT COUNT(orders_table.product_quantity) AS number_of_sales, SUM(orders_table.product_quantity) AS product_quantity_count, Loc_Subq.location AS location
  FROM orders_table 
  JOIN
    (
    SELECT store_code, 
    CASE 
        WHEN store_type = 'Web Portal' THEN 'Web'
        ELSE 'Offline'
    END AS location
    FROM dim_store_details
    ) AS Loc_Subq
  ON orders_table.store_code= Loc_Subq.store_code
GROUP BY location
ORDER BY number_of_sales ASC ;