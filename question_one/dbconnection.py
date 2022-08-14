import pandas as pd
import configparser
from sqlalchemy import create_engine
import sqlalchemy
import urllib.parse

from helper_function import handle_exception


class DBConnection:
    """
        Class that handles connection and Query execution

        PARAMETER:
        
        parse_class: Class that handles parsing of dataframe
        chunksize: Determines number of record pulled at a time

    """
    def __init__(self,parse_class,chunksize=50000):
        self.parse_class = parse_class
        self.chunksize = chunksize
    def db_conn(self,conn_param = 'DB_CONNECTION'):
        """
        
        Creates a Database connection from configuration file
        Parameters
        ----------
        conn_param : str 
                    default : DB_CONNECTION
    
        Returns
        -------
        db engine :
        db connection :
        """
        config = configparser.ConfigParser()
        config.read('config.ini')
        POSTGRES_ADDRESS = config[conn_param]['POSTGRES_ADDRESS']
        POSTGRES_PORT = config[conn_param]['POSTGRES_PORT']
        POSTGRES_USERNAME = config[conn_param]['POSTGRES_USERNAME']
        POSTGRES_PASSWORD = urllib.parse.quote_plus(config[conn_param]['POSTGRES_PASSWORD'])
        POSTGRES_DBNAME = config[conn_param]['POSTGRES_DBNAME']

        conn_str = f'postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_ADDRESS}:{POSTGRES_PORT}/{POSTGRES_DBNAME}'
        
        try:
            engine = create_engine(conn_str)
            conn = engine.connect()
        except (sqlalchemy.exc.DBAPIError,sqlalchemy.exc.InterfaceError) as err:
            print('database could not connect\n', err)
            engine = None
            conn = None
        finally:
            return engine,conn


    def execute_sql(self,filename,ddl = True):
        """
        This takes in a sql file and execute in the database

        PARAMETERS
        -----------------------------------
        filename:
            Type: str
            Description: name of sql file. Absolute path to the sql file needs to be included
        ddl:
            Type: Boolean
            Description: This parameter specified if DDL is to be executed
        """
        engine,conn = self.db_conn()
        with open(filename,'r') as f:
            if ddl:
                try:
                    # for script in f.read().split(';'):
                    conn.execute(f.read())
                except Exception as err:
                    handle_exception(err)
            else:
                dframes = pd.read_sql(f.read(),engine,chunksize=self.chunksize)
                for dframe in dframes:
                    dframe.to_csv('output.csv')
        conn.close()
        engine.dispose()


    def upsert(self,tablename,dframes):    
        """
            This function loads data from dataframe into the database

            PARAMETERS
            ----------------------------------------
            tablename: Name of table in database
            dframe: iterator object of dataframe

        """
        engine,conn = self.db_conn()
        for df in dframes:
            try : 
                df = self.parse_class.change_column_dtype(df)
                columns = [col.replace('(','_').replace(')','') for col in list(df.columns)]
                df.columns = columns
                df.to_sql(tablename,engine, index=False, if_exists="append")
            except Exception as err:
                handle_exception(err)
                
        conn.close()
        engine.dispose()   