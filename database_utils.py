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
        Need to pip install PyYAML and import yaml to do this
        '''        
        with open(yaml_file, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
        return data_loaded

    @staticmethod
    def init_db_engine(yaml_file):        
        '''
        Now create a method init_db_engine which will read the credentials from the return of read_db_creds 
        and initialise and return an sqlalchemy database engine.
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
    The method below is only applicable to the remote RDS database, 
    so this needs to be defined in an inherited class.
    '''
    def list_db_tables(self):        
        '''
        Using the engine from init_db_engine create a method list_db_tables to list all the tables 
        in the database so you know which tables you can extract data from.
        Develop a method inside your DataExtractor class to read the data from the RDS database.
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
        This method will take in a Pandas DataFrame and table name to upload to as an argument.
        '''
        df.to_sql(table_name, self.engine, if_exists='replace')
