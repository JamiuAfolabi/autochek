import pandas as pd
from parse import Parse

from dbconnection import DBConnection
import configparser

from helper_function import handle_exception


config = configparser.ConfigParser()
config.read('config.ini')

conn_param = 'DATA'
borrower_table_url = config[conn_param]['BORROWER_URL']
loan_data_url = config[conn_param]['LOAN_DATA_URL']
payment_schedule_url = config[conn_param]['PAYMENT_SCHEDULE_URL']
repayment_data_url = config[conn_param]['REPAYMENT_DATA_URL']


create_table_script = config[conn_param]['CREATE_TABLE_SCRIPT']
result_script = config[conn_param]['RESULT_SCRIPT']


if __name__=='__main__':
    # Intitialization of the classes
    parse = Parse()
    db = DBConnection(parse)

    try:
        # Read data from google sheet
        borrower_df = pd.read_csv(parse.parse_url(borrower_table_url),iterator=50000)
        loan_df = pd.read_csv(parse.parse_url(loan_data_url),iterator=50000)
        payment_schedule_df = pd.read_csv(parse.parse_url(payment_schedule_url),iterator=50000)
        repayment_data_df = pd.read_csv(parse.parse_url(repayment_data_url),iterator=50000)

        # Create required tables
        db.execute_sql(ddl=True,filename = create_table_script)
        db.upsert('borrower',borrower_df)
        db.upsert('loan_data',loan_df)
        db.upsert('payment_schedule',payment_schedule_df)
        db.upsert('repayment_data',repayment_data_df)

        # Export result to file
        db.execute_sql(ddl=False,filename=result_script) 
    except Exception as err:
        handle_exception(err)