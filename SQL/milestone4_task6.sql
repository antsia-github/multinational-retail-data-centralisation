--Task 6 : The month and year with the most sales------------
SELECT 
       SUM(orders_table.product_quantity * dim_products.product_price) as total_sales, 
       dim_date_times.year AS year, dim_date_times.month AS month 
FROM orders_table
     JOIN dim_date_times ON orders_table.date_uuid = dim_date_times.date_uuid 
     JOIN dim_products ON orders_table.product_code = dim_products.product_code
GROUP BY year, month
ORDER BY total_sales DESC 
LIMIT 10;