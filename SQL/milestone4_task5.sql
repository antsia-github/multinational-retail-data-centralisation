--Task 5------
SELECT dim_store_details.store_type AS store_type, 
SUM(orders_table.product_quantity * dim_products.product_price) as total_sales,
SUM(orders_table.product_quantity * dim_products.product_price)*100/
(SELECT SUM(orders_table.product_quantity * dim_products.product_price)
FROM orders_table
JOIN dim_products
on orders_table.product_code = dim_products.product_code
) AS percentage_total
FROM orders_table
JOIN dim_store_details
on orders_table.store_code = dim_store_details.store_code 
JOIN dim_products
on orders_table.product_code = dim_products.product_code
GROUP BY store_type
ORDER BY total_sales DESC 
LIMIT 6;