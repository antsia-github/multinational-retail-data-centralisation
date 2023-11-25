import tabula
import boto3
from sqlalchemy import text
from database_utils import DatabaseConnector
import pandas as pd
import tabula
import requests

@staticclass
class DataExtractor:
    '''
    This class will work as a utility class, where the methods help extract data 
    from different data sources. The methods contained will be fit to extract data 
    from a particular data source, these sources will include CSV files, an API and an S3 bucket.
    '''
    def extract_from_s3(uri):
        '''
        extract product information (stored in an S3 bucket) from AWS.
        Args:
            uri (URI): the S3 address
        '''
        s3 = boto3.client('s3')
        #URI starts with 's3://', so we need to remove this first 5 characters.
        bucket,obj = uri[5:].split('/')
        #download the file, name it S3Obj.csv, then load it as a pandas dataframe
        s3.download_file(bucket, obj, './S3Obj.csv') 
        df = pd.read_csv('./S3Obj.csv')
        return df

    def read_rds_table(db_conn_obj,table_name):
        """
        Args:
            db_conn_obj (DatabaseConnector): connector to the AWS RDS database  
            table_name (str): table name keyword
        """
        list_tables = db_conn_obj.list_db_tables()
        # find all table names which contain the string table_name  
        list_tables_correct = [table for table in list_tables if table_name in table.lower()]
        correct_name = list_tables_correct[0] # get the first occurence         

        df = pd.read_sql_table(correct_name, db_conn_obj.engine)        
        return df

    def retrieve_pdf_data(pdf_path):
        ''' extract all pages from pdf document. 
        Args:
            pdf_path (string): path to the pdf document
        '''
        dfs = tabula.read_pdf(pdf_path, pages='all')              
        return pd.concat(dfs)

    def list_number_of_stores(url, headers):
        '''
        This method returns the number of stores to extract. 
        It takes in the endpoint and header dictionary as an argument.
        '''
        # GET request with custom header
        response = requests.get(url,headers=headers)
        return response

    def retrieve_stores_data(url, headers, num_stores):
        '''
        This method takes the retrieve a store endpoint as an argument and extracts 
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
