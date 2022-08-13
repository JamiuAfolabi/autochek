import pandas as pd
import os

dir_path = os.path.dirname(os.path.realpath(__file__))



def upsert_database(data,target_engine,schema_name):

    """
        insert and update data to a destination database table

        Parameters
        ----------
        data : dataframe
            data to upsert into Destination DB table

        schema_name : str
            name of the schema that contains the table to be upserted in the destination DB
        
        target_engine : sql engine
            database connection engine 

        
    """
    # create the table if it does not exist with the timestamp and currency_to as composite keys
    # to aviod duplicated data
    target_engine.execute(f"""CREATE TABLE IF NOT EXISTS {schema_name}.rate( 
                            timestamp TIMESTAMP,
                            currency_from CHAR(3),
                            USD_to_currency FLOAT8,
                            currency_to_USD FLOAT8,
                            currency_to CHAR(3) ,
                            PRIMARY KEY(timestamp,currency_to))
                            """)
    #upsert the table records                    
    target_engine.execute(
        f"""
        INSERT INTO {schema_name}.rate(timestamp,currency_from,USD_to_currency,currency_to_USD,currency_to)
                VALUES {','.join([str(i) for i in list(data.to_records(index=False))])}
                ON CONFLICT(timestamp,currency_to)
                DO UPDATE SET currency_from= excluded.currency_from,
                               USD_to_currency= excluded.USD_to_currency,
                               currency_to_USD = excluded.currency_to_USD
        """
    )
    
def load_to_local(data):
    
    """
        save data from website locally

        Parameters
        ----------
        data : dataframe
            data to upsert into Destination DB table
    """

    # create a csv file to save historical data if it does not exist
    try :
        historical_data =  pd.read_csv(f'{dir_path}/historical_data.csv')
    except :
        historical_data = pd.DataFrame(columns=['timestamp' , 'currency_from', 'USD_to_currency', 'currency_to_USD' ,'currency_to'])
    
        #append new records to historical data
        historical_data = pd.concat([historical_data,data],axis= 0)
        historical_data = historical_data.reset_index(drop =  True)

        # drop duplicates if records are entered the same day
        historical_data = historical_data.drop_duplicates(subset=['timestamp' ,'currency_to'],keep = 'first')

        # overwrite existing transaction 
        historical_data.to_csv(f'{dir_path}/historical_data.csv',index = False)



