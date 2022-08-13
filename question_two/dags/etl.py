
import configparser
import ast
from datetime import datetime
from webbrowser import get
import pandas as pd
import os
from credentials import  db_conn
from extract import get_exchange
from load import upsert_database,load_to_local

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta
from airflow.utils.dates import days_ago


dir_path = os.path.dirname(os.path.realpath(__file__))
config = configparser.ConfigParser()
config.read(f"{dir_path}/config.ini")

 #load config for the website and the destination database
config_source = 'SOURCE'
config_target = 'DESTINATION'
currencies =  ast.literal_eval(config[config_source]["currencies"])  #currencies to load online
account_id = config[config_source]["account_id"] # website account id
api_key = config[config_source]["api_key"]  # website account api key
target_schema = config[config_target]["schema"] # destination database schema


# def run_etl():
   
#     try:
#     # extract currency exchange rate from the target website
#         currency_data =  get_exchange(currencies=currencies,account_id=account_id,api_key=api_key)

#         # load currency exchange rate to csv file_locally
#         load_to_local(data =currency_data)

#         #load currency exchange rate into a database

#         target_engine,conn_target =  db_conn(conn_param=config_target) # establish the database connection
#         upsert_database(data= currency_data,target_engine=target_engine,schema_name=target_schema)
#     except Exception as err:
#         print(err)

currency_data =  get_exchange(currencies=currencies,account_id=account_id,api_key=api_key)
target_engine,conn_target =  db_conn(conn_param=config_target)

default_args = {
        'owner': 'airflow',
        'retry_delay': timedelta(minutes=30),
        'start_date': datetime(2022, 8, 13),
        'schedule_interval': '0 11,1 * * *'
    }

with DAG(
    dag_id="currency",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['currency_extractor'],
    ) as dag:

        load_to_file = PythonOperator(task_id='load_to_local', 
                                    python_callable=load_to_local, 
                                    op_kwargs = {'data':currency_data}
                                    )
        load_to_database = PythonOperator(task_id='load_to_database', 
                                    python_callable=upsert_database, 
                                    op_kwargs = {'data':currency_data,
                                                'target_engine': target_engine,
                                                'schema_name': target_schema
                                    }
                                    )

        # python_task
        load_to_file
        load_to_database

