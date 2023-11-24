import tabula
import boto3
from sqlalchemy import text
from database_utils import DatabaseConnector
import pandas as pd
import tabula
import requests

class DataExtractor:
    '''
    This class will work as a utility class, in it you will be creating methods that help extract data 
    from different data sources. The methods contained will be fit to extract data from a particular 
    data source, these sources will include CSV files, an API and an S3 bucket.
    '''
    def __init__(self):
        pass

    def extract_from_s3(self, uri):
        '''
        The information for each product the company currently sells is stored in CSV format in an S3 bucket 
        on AWS.
        Step 1:
        Create a method in DataExtractor called extract_from_s3 which uses the boto3 package to download 
        and extract the information returning a pandas DataFrame.

        The S3 address for the products data is the following s3://data-handling-public/products.csv 
        the method will take this address in as an argument and return the pandas DataFrame.
        '''
        s3 = boto3.client('s3')
        #URI starts with 's3://', so we need to remove this first 5 characters.
        bucket,obj = uri[5:].split('/')
        #download the file, name it S3Obj.csv, then load it as a pandas dataframe
        s3.download_file(bucket, obj, './S3Obj.csv') 
        df = pd.read_csv('./S3Obj.csv')
        return df

    def read_rds_table(self, db_conn_obj,table_name):
        """
        Develop a method called read_rds_table in your DataExtractor class which will extract the database table 
        to a pandas DataFrame.
        It will take in an instance of your DatabaseConnector class and the table name as an argument 
        and return a pandas DataFrame.
        Use your list_db_tables method to get the name of the table containing user data.
        Use the read_rds_table method to extract the table containing user data and return a pandas DataFrame.
        """
        list_tables = db_conn_obj.list_db_tables()
        # find all table names which contain the string table_name  
        list_tables_correct = [table for table in list_tables if table_name in table.lower()]
        correct_name = list_tables_correct[0] # get the first occurence         

        df = pd.read_sql_table(correct_name, db_conn_obj.engine)        
        return df

    def retrieve_pdf_data(self, pdf_path):
        '''This method takes in a link as an argument and returns a pandas DataFrame.
        Using the tabula-py Python package, extract all pages from the pdf document 
        at following link. Then return a DataFrame of the extracted data.
        '''
        dfs = tabula.read_pdf(pdf_path, pages='all')              
        return pd.concat(dfs)

    def list_number_of_stores(self, url, headers):
        '''
        This method returns the number of stores to extract. It should take in the number of stores endpoint 
        and header dictionary as an argument.
        '''
        # GET request with custom header
        response = requests.get(url,headers=headers)
        return response

    def retrieve_stores_data(self, url, headers, num_stores):
        '''
        This method will take the retrieve a store endpoint as an argument and extracts 
        all the stores from the API saving them in a pandas DataFrame.
        '''
        listdict = []
        for id in range(num_stores):
            #url ='https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/'
            response = requests.get(url + str(id) ,headers=headers)
            if response.status_code < 300:
                listdict.append(response.json())
            else:
                pass
        return pd.DataFrame(listdict)
