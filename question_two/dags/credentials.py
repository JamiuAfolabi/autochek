import configparser
from sqlalchemy import create_engine
import sqlalchemy
import urllib.parse
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read(f"{dir_path}/config.ini")

def db_conn(conn_param ):

    """

       creates and return  a database connection

        Parameters
        ----------
        conn_param : config
                schema : schema_name
                POSTGRES_ADDRESS : link DB on cloud
                POSTGRES_PORT : port
                POSTGRES_USERNAME 
                POSTGRES_PASSWORD 
                POSTGRES_DBNAME 

           

        Returns
        -------
         
            database engine , database connection
    """
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




    
