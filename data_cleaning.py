import re
import pandas as pd
from dateutil.parser import parse
import numpy as np

def parse_date_retain(x):
    '''parsing correct date data but retain the incorrect ones. The result will be passed to date_time'''
    try:
       y = parse(x)
    except: 
       y = x
    return y 


def clean_weight(s):
    '''This method is used to convert ...
    '''
    s = str(s)
    m=re.search('^([0-9x.]+)([a-zA-Z]+)$', s)  # to capture decimal and multiplication   
    if m:
        mgr=m.groups()
        if len(mgr) == 2:
            if 'x' in mgr[0]:
                qtyx = mgr[0].split('x')
                qty = float(qtyx[0])*float(qtyx[1])
            else:
                qty = float(mgr[0])
                
            unitw = mgr[1].lower()

            if unitw == 'kg':
                weight = qty
            elif unitw == 'g':
                weight = qty/1000.0
            elif unitw == 'ml':
                weight = qty/1000.0
            elif unitw == 'oz':
                weight = qty/10.0                
            else:
                weight = np.nan # float('NaN')
        else:
            weight = np.nan #float('NaN')   
    else:
        weight = np.nan # float('NaN')
    return weight   

class DataCleaning:
    '''
    This class contains methods to clean data from each of the data sources.
    It will need to clean the user data, look out for NULL values, errors with dates, incorrectly typed values 
    and rows filled with the wrong information.
    '''

    def __init__(self):
        pass

    def clean_user_data(self, df):
        '''
        This method will perform the cleaning of the user data.
        It will clean the user data, look out for NULL values, errors with dates, 
        incorrectly typed values and rows filled with the wrong information.
        '''
        df['join_date'] = df.join_date.apply(parse_date_retain)
        df['join_date'] = pd.to_datetime(df.join_date, infer_datetime_format=True, errors='coerce')

        df['date_of_birth'] = df.join_date.apply(parse_date_retain)
        df['date_of_birth'] = pd.to_datetime(df.join_date, infer_datetime_format=True, errors='coerce')

        df.dropna(inplace=True)

        return df

    def clean_card_data(self, df):
        '''
        This method cleans the data to remove any erroneous values, NULL values or errors with formatting.
        '''
        #The card number needs a number of cleaning steps
        #Several cells have 'NULL' string value 
        df.replace('NULL',np.NaN, inplace=True)
        df.drop_duplicates(inplace=True)
        #Need to delete NaN data to make the subsequent cleaning steps easier 
        df.dropna(inplace=True)
        
        #It seems that some rows have integer and others are string
        df.card_number = df.card_number.apply(str) 

        #Some rows start with some '?' characters followed by valid digits 
        df.card_number = df.card_number.apply(lambda x: x.replace('?',''))
        
        #Need to drop rows which have card number with some alphabet values
        #df = df.drop(df[~ df.card_number.str.isdigit()].index)
        #The above does not work as intended, so the following is used instead
        df.card_number = df.card_number.apply(lambda x: x if all(i.isdigit() for i in x) else np.nan)

        df.dropna(inplace=True)
        return df

    def clean_store_data(self, df):
        '''
        This method cleans the data retrieved from the API and returns a pandas DataFrame.
        '''
        df.longitude = pd.to_numeric(df.longitude, errors='coerce')
        df.latitude = pd.to_numeric(df.latitude, errors='coerce')
        df.staff_numbers = pd.to_numeric(df.staff_numbers, errors='coerce')

        #we can't use dropna(axis=0, inplace=True), it will remove 'lat' (mostly Null). lat will be removed in Milestone 3 (through SQL operation).
        #df.dropna(axis=0, inplace=True) 

        df.opening_date = df.opening_date.apply(parse_date_retain)
        df.opening_date = pd.to_datetime(df.opening_date, infer_datetime_format=True, errors='coerce')
 
        #this does not remove the NULL in store_code, it seems the 'NULL' is a string 
        df['store_code'][df['store_code']=='NULL'] = np.nan
        df.dropna(subset=['store_code'],inplace=True)

        #all rows with invalid country code do not give meaningful information 
        df.country_code=df.country_code.apply(lambda x: x if len(x) <= 3 else np.nan)
        df.dropna(subset=['country_code'], inplace=True)

        return df
    
    def convert_product_weights(self, df):
        '''
        This method will take the products DataFrame as an argument and return the products DataFrame.
        If you check the weight column in the DataFrame the weights all have different units.
        Convert them all to a decimal value representing their weight in kg. Use a 1:1 ratio of ml to g as a rough estimate for the rows containing ml.
        Develop the method to clean up the weight column and remove all excess characters then represent the weights as a float.
        '''
        #removing large value represented by NaN 
        df.dropna(inplace=True) 

        #remove dot and space at the end of the string
        df['weight'] = df['weight'].apply(lambda x: x[:-1].replace(" ", "") if not x[-1].isalnum() else x.replace(" ", "")) 

        #convert all the weight to kg
        df['new_weight'] = df['weight'].apply(clean_weight)     
        df.drop(['weight'], axis=1, inplace=True)
        df.rename(columns={'new_weight' : 'weight'}, inplace=True)

        return df
    
    def clean_products_data(self, df):
        '''
        Tthis method will clean the DataFrame of any additional erroneous values.
        '''
        #remove all rows which have NaN after being filtered by clean_weight                
        df.dropna(inplace=True) 
        return df

    def clean_orders_data(self, df):
        '''
        Task 7 Step 3:
        This method will clean the orders table data.
        You should remove the columns, first_name, last_name and 1 to have the table in the correct form 
        before uploading to the database.
        You will see that the orders data contains column headers which are the same in other tables.
        This table will act as the source of truth for your sales data and will be at the center of your star based database schema.
        '''
        
        df.drop(['first_name', 'last_name', '1', 'level_0'], axis=1, inplace=True)
        return df

    def clean_date_times_data(self, df):
        '''
        The final source of data is a JSON file containing the details of when each sale happened, 
        as well as related attributes.
        The file is currently stored on S3 and can be found at the following link https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json.
        Extract the file and perform any necessary cleaning, then upload the data to the database naming 
        the table dim_date_times.
        '''
        df['day']=df['day'].apply(lambda x: x if len(x)<=2 else np.nan)
        df['month']=df['month'].apply(lambda x: x if len(x)<=2 else np.nan)
        df.dropna(inplace=True)
        return df