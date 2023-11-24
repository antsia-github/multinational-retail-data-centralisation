--Task 6------------
SELECT SUM(orders_table.product_quantity * dim_products.product_price) as total_sales, dim_date_times.year AS year, dim_date_times.month AS month 
FROM orders_table
JOIN dim_date_times
on orders_table.date_uuid = dim_date_times.date_uuid 
JOIN dim_products
on orders_table.product_code = dim_products.product_code
GROUP BY year, month
ORDER BY total_sales DESC 
LIMIT 10;