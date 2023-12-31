----Task 8 : Top total sales by store type in Germany 
SELECT  
        SUM(orders_table.product_quantity * dim_products.product_price) as total_sales,
        dim_store_details.store_type AS store_type,
        dim_store_details.country_code AS country_code
FROM orders_table
        JOIN dim_store_details ON orders_table.store_code = dim_store_details.store_code 
        JOIN dim_products ON orders_table.product_code = dim_products.product_code
WHERE country_code = 'DE'
GROUP BY store_type, country_code
ORDER BY total_sales ASC
LIMIT 4;