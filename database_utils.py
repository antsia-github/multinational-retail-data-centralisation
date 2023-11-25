import yaml
from sqlalchemy import create_engine
from sqlalchemy import inspect

class DatabaseConnector:
    '''
    This class is used to connect with and upload data to the database.
    '''
    def __init__(self, yaml_file):
       self.engine = self.init_db_engine(yaml_file)       

    @staticmethod
    def read_db_creds(yaml_file):    
        '''
        This method will read the credentials yaml file and return a dictionary of the credentials.
        '''        
        with open(yaml_file, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
        return data_loaded

    @staticmethod
    def init_db_engine(yaml_file):        
        '''
        create a method which will read the credentials and 
        initialise and return an sqlalchemy database engine.
        '''
        dict_cred = __class__.read_db_creds(yaml_file) 
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = dict_cred['RDS_HOST']
        USER = dict_cred['RDS_USER']
        PASSWORD = dict_cred['RDS_PASSWORD']
        DATABASE = dict_cred['RDS_DATABASE']
        PORT = dict_cred['RDS_PORT']        
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        engine.connect()
        return engine

    def close_db_engine(self):
        self.engine.close()


class RDSConnector(DatabaseConnector):
    '''
    A subclass for the remote RDS database connection
    '''
    def list_db_tables(self):        
        '''
        list all the tables in the database that can be extracted.
        '''
        inspector = inspect(self.engine)
        return inspector.get_table_names()

class LocalConnector(DatabaseConnector):
    ''' 
    This derived class is used since it needs an upload method to update the DB. 
    This is not used in the RDSConnector since we do not want to edit the remote database.
    '''
    def upload_to_db(self, df, table_name):
        '''
        upload a Pandas DataFrame to a specific table in the local DB. 
        '''
        df.to_sql(table_name, self.engine, if_exists='replace')
