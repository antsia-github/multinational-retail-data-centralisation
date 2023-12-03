
----Task 1: Changing datatypes in the orders_table ----
----using "SELECT MAX(LENGTH(var_name)) FROM orders_table" for var_name = [store_code, product_code, card_number]
----to obtain the maximum length of varchar 
ALTER TABLE orders_table
    ALTER COLUMN date_uuid SET DATA TYPE UUID  USING date_uuid::uuid,
    ALTER COLUMN user_uuid SET DATA TYPE UUID  USING user_uuid::uuid,
    ALTER COLUMN product_quantity TYPE SMALLINT,
    ALTER COLUMN store_code TYPE VARCHAR(12),
    ALTER COLUMN product_code TYPE VARCHAR(11),
    ALTER COLUMN card_number TYPE VARCHAR(19);


-------Task 2: Changing datatypes in dim_users------
ALTER TABLE dim_users
    ALTER COLUMN join_date TYPE DATE using(join_date::date),
    ALTER COLUMN date_of_birth TYPE DATE using(date_of_birth::date),
    ALTER COLUMN first_name TYPE varchar(255),
    ALTER COLUMN last_name TYPE varchar(255),       
    ALTER COLUMN country_code TYPE varchar(3),           
    ALTER COLUMN user_uuid SET DATA TYPE UUID  USING user_uuid::uuid;
  

--------Task 3: Dropping the lat variable and changing datatypes in dim_store_details---------
ALTER TABLE dim_store_details
    DROP COLUMN lat;

ALTER TABLE dim_store_details
    ALTER COLUMN opening_date TYPE DATE using(opening_date::date),
    ALTER COLUMN longitude TYPE FLOAT,
    ALTER COLUMN latitude TYPE FLOAT,
    ALTER COLUMN locality TYPE varchar(255),
    ALTER COLUMN continent TYPE varchar(255),
    ALTER COLUMN store_type TYPE varchar(255),       
    ALTER COLUMN store_code TYPE varchar(12),
    ALTER COLUMN country_code TYPE varchar(3),
    ALTER COLUMN staff_numbers TYPE smallint;
 
--------Task 4-----------------
--------Delete the £ symbol from price column 
UPDATE dim_products
    SET product_price = REPLACE(product_price, '£', '');

-------Setting a new variable weight_class
ALTER TABLE dim_products 
    ADD COLUMN weight_class varchar(14);
--Change into categorical values 
UPDATE dim_products
SET weight_class =
    (CASE
        WHEN weight < 2 THEN 'Light'
        WHEN weight BETWEEN 2 AND 40 THEN 'Mid_Sized'
        WHEN weight BETWEEN 40 AND 140 THEN 'Heavy'
        WHEN weight >= 140 THEN 'Truck_Required'
        END 
    );



---------Task 5: : Changing name and values of a variable and datatypes in dim_products--------------
------Rename removed variable
ALTER TABLE dim_products
    RENAME removed TO still_available;

------Setting new categorical values  
UPDATE dim_products
SET still_available =
(CASE
    WHEN still_available = 'Still_avaliable' THEN 'Yes'
    WHEN still_available = 'Removed' THEN 'No'
    END 
);

-------Changing the datatypes
ALTER TABLE dim_products
    ALTER COLUMN "EAN" TYPE varchar(17),
    ALTER COLUMN product_code TYPE varchar(11),  
    ALTER COLUMN uuid SET DATA TYPE UUID  USING uuid::uuid,
    ALTER COLUMN date_added TYPE DATE using(date_added::date),
    ALTER COLUMN weight TYPE FLOAT,
    ALTER COLUMN still_available TYPE bool USING CASE WHEN still_available='Yes' THEN TRUE ELSE FALSE END,
    ALTER COLUMN product_price TYPE FLOAT using product_price::FLOAT;


------ Task 6 : Changing datatypes in dim_date_times -----
ALTER TABLE dim_date_times
    ALTER COLUMN month TYPE varchar(2),
    ALTER COLUMN year TYPE varchar(4),
    ALTER COLUMN day TYPE varchar(2),
    ALTER COLUMN time_period TYPE varchar(10), 
    ALTER COLUMN date_uuid SET DATA TYPE UUID  USING date_uuid::uuid;


-----------Task :  Changing datatypes in dim_card_details ----------------
ALTER TABLE dim_card_details
    ALTER COLUMN card_number TYPE varchar(19),
    ALTER COLUMN expiry_date TYPE varchar(10),
    ALTER COLUMN date_payment_confirmed TYPE DATE using(date_payment_confirmed::date);


--------Task 8: Adding primary keys----------
ALTER TABLE dim_users ADD PRIMARY KEY (user_uuid);
ALTER TABLE dim_store_details ADD PRIMARY KEY (store_code);
ALTER TABLE dim_products ADD PRIMARY KEY (product_code);  
ALTER TABLE dim_date_times ADD PRIMARY KEY (date_uuid);
ALTER TABLE dim_card_details ADD PRIMARY KEY (card_number);



---------------Task 9: Adding foreign keys-----------
ALTER TABLE orders_table 
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_uuid) REFERENCES dim_users (user_uuid),
    ADD CONSTRAINT fk_store_id FOREIGN KEY (store_code) REFERENCES dim_store_details (store_code),
    ADD CONSTRAINT fk_date_id FOREIGN KEY (date_uuid) REFERENCES dim_date_times (date_uuid),    
    ADD CONSTRAINT fk_card_id FOREIGN KEY (card_number) REFERENCES dim_card_details (card_number),    
    ADD CONSTRAINT fk_product_id FOREIGN KEY (product_code) REFERENCES dim_products (product_code);       
