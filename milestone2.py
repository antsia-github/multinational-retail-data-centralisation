from database_utils import RDSConnector, LocalConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning
import pandas as pd
import requests

#initialise AWS RDS DB engine 
dbc_rds = RDSConnector('db_creds.yaml')
#initialise local postgre DB engine 
dbc_local = LocalConnector('postgre_db_local.yaml')
#instances of Data Extractor and Data Cleaning classes
dataxtr = DataExtractor()
dcl = DataCleaning()

#-------Task 3, Milestone 2
print('-----Task 3------')
# extract the user data from RDS
# calling this will invoke the method dbc_rds.list_db_tables
df_user = dataxtr.read_rds_table(dbc_rds,'user') 
df_user = dcl.clean_user_data(df_user)

# upload the cleaned dataframe to the local database
dbc_local.upload_to_db(df_user,'dim_users')

#-------Task 4, Milestone 2
print('-----Task 4------')
# extract the card data from Amazon storage
df_card = dataxtr.retrieve_pdf_data("https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf")
df_card = dcl.clean_card_data(df_card)

# upload the cleaned dataframe to the local database
with dbc_local.engine.begin() as connection:
    dbc_local.upload_to_db(df_card,'dim_card_details')

#-------Task 5, Milestone2
print('-----Task 5------')
#get the information of the number of stores with API
url_num = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
headers = {"x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"}
response = dataxtr.list_number_of_stores(url_num, headers)

datadict = response.json()
num_stores = datadict['number_stores']
print('Number of stores =' , num_stores)

#---grab the data from all stores (it needs the same authentication headers) and store it as a pandas dataframe 
url_store ='https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/'
df_store = dataxtr.retrieve_stores_data(url_store, headers, num_stores)

df_store = dcl.clean_store_data(df_store)

# upload the cleaned dataframe to the local database
with dbc_local.engine.begin() as connection:
    dbc_local.upload_to_db(df_store,'dim_store_details')


#-------Task 6, Milestone2-----------------
print('-----Task 6------')
#extract the product data from URI
uri = 's3://data-handling-public/products.csv'
df_prod = dataxtr.extract_from_s3(uri)

df_prod= dcl.convert_product_weights(df_prod)
df_prod = dcl.clean_products_data(df_prod)

# upload the cleaned dataframe to the local database
with dbc_local.engine.begin() as connection:
    dbc_local.upload_to_db(df_prod,'dim_products')


#-------Task 7, Milestone2-----------------
print('-----Task 7------')
# extract the order data from RDS
df_order = dataxtr.read_rds_table(dbc_rds,'order')
df_order = dcl.clean_orders_data(df_order)

# upload the cleaned dataframe to the local database
with dbc_local.engine.begin() as connection:
    dbc_local.upload_to_db(df_order,'orders_table')

#-------Task 8, Milestone2-----------------
print('-----Task 8------')
# extract the date data from Amazon storage
urls3 = 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'
response = requests.get(urls3)
datajson = response.json()
df_date = pd.DataFrame(datajson)
df_date = dcl.clean_date_times_data(df_date)

# upload the cleaned dataframe to the local database
with dbc_local.engine.begin() as connection:
    dbc_local.upload_to_db(df_date,'dim_date_times')

print('-----Finished------')