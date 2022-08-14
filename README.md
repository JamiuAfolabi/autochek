# autochek

# Problem One 

## Problem Statement

The overall goal starts by getting our dealers to list
their cars, displaying these cars to the prospective customers on our marketplace and then
providing affordable car loans to make life easy, you as our data engineer suddenly gets a
data request around one of our most delicate dataset, Apparently, the business leaders
would like to see a summarized table generated from data of the customer
(borrower_table), the loans they currently have(loans table), the dates they have been
scheduled to repay (payment_schedule), how frequent they are paying back
(loan_payment), lastly a table that shows, history of times customers have missed their
payments (missed_payment)

## This repository contains:

- User-defined functions (UDFs)
- Airflow DAGs for scheduled python-etl scripts

1.[Pre-requisites](#Pre-requisites)

2.[DATA_TRANSFORMATION](#DATA_TRANSFORMATION) 

3.[IMPLEMENTATION WITH PYTHON](#IMPLEMENTATION-WITH-PYTHON)

4.[IMPLEMENTATION WITH PYTHON AND SQL](#IMPLEMENTATION-WITH-PYTHON-AND-SQL)

5.[STEPS-TO-RUN-CODE](#STEPS)


## Pre-requisites

- **Python 3.8+** - see [this guide](https://docs.python-guide.org/starting/install3/win/) for instructions if you're on a windows. 
- **Requirement.txt** - see [this guide](https://note.nkmk.me/en/python-pip-install-requirements/) on running a requirement.txt file.
- **Airflow** - (required for orchestration. [Airflow Installation Guide](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html)).
--Airflow was preferred to crontab for orchestration because it offers the ability to schedule, monitor, and most importantly, scale, increasingly complex workflows.
- **Docker** - (needed for contenarization). [Docker Installation Guide](https://docs.docker.com/desktop/install/)).



### DATA_TRANSFORMATION

This project was aimed at generating a transformed data for the business.

The data was studied and analyzed to get an overview of the project. Findings include:

  - Some dates were out of range, hence a function was designed to parse the dates.
  - The borrower_credit_score 
  
  - The tables form a star schema has shown in the ERD diagram
  
  ![alt text](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/ERD.PNG)

  - There is a relationship between the payment_schedule and repayment_data via the schedule_id and payment_id_pk.
    The payment_id_pk was parsed by excluding Substring "PAID". The resulting output was a foreign key from the payment_schedule table

Three approaches were considered

### IMPLEMENTATION-WITH-PYTHON

    This approach involves executing all logic of the code in python. The bulk of the transformation was carried out in pandas.
    It comes with ease developing a production ready code at a fast pace.
    
    However, this is not suitabl for very large datasets due to memory constraint and its inability to support multiprocessing.
    
    A notebook implementation is included
    
 
    
   [Notebook implementation](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/python_solution_two.ipynb)
   
   The [Result](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/output2.csv) was generated as a CSV.


### IMPLEMENTATION-WITH-PYTHON-AND-SQL


   This involves ingesting the data from the source to an SQL Database. This provides a memory store and processing power is shared
   by the driver node(system running the python script) and the database engine. It also provides a persistent store where other BI tools
   can easily integrate.
   
   An ETL pipeline was built to ingest data from Google Sheet to Postgres on Dockers Container. All Exceptions are logged in 
   [logs.txt](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/logs.txt).
   This is important for debugging purpose
   
   #### STEPS
   - Include necessary database parameters in the [CONFIG](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/config.ini) file.       POSTGRES_ADDRESS is the IP of the server dockers is running.  
   - Startup the [Postgres](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/docker-compose.yml) docker container. 
    
          docker-compose up
    
   - Execute the [Main.py](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/main.py) script. This script 
        - Create [DB Connection](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/dbconnection.py)
        - [Transform](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/parse.py) the data parsed
        - Creates table using [Relationship.sql](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/relationship.sql) and ingest the data
        - Execute [Result.sql](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/result.sql) script to generate the desired output
        - Save the result in [Output.csv](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/output.csv)
 

### IMPLEMENTATION-WITH-PYSPARK
  - This method is highly efficient when integrated with HDFS. This should be considered when the dataset is very large. It supports Multiprocessing,
    hence, increasing the speed of transformation

# Problem Two





# Xe Currency Rate ETL
An example on how to build a data ETL pipeline from Xe's API

## Problem Statement 

we would like to get all our exchange rate from one source, code up a script
that gets the rate of 7 countries and a scheduler to pull this rate 2 times a day, first at 1am
and second at 11pm. Rates should be saved per day meaning, no duplicate records for a
single date.
- Rate website url → https://www.xe.com/xecurrencydata/
- Rate website doc → https://xecdapi.xe.com/docs/v1/

## This repository contains:

- User-defined functions (UDFs)
- Airflow DAGs for scheduled python-etl scripts

1.[Pre-requisites](#Pre-requisites)

2.[Data Engineering Structure](#data-engineering-structure)

3.[Extract Data](#Extract_Data)

4.[Load Data](#Load_Data)




## Pre-requisites

- **Python 3.8+** - see [this guide](https://docs.python-guide.org/starting/install3/win/) for instructions if you're on a windows. 
- **Requirement.txt** - see [this guide](https://note.nkmk.me/en/python-pip-install-requirements/) on running a requirement.txt file.
- **Airflow** - (required for orchestration. [Airflow Installation Guide](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html)).
--Airflow was preferred to crontab for orchestration because it offers the ability to schedule, monitor, and most importantly, scale, increasingly complex workflows.
- **Docker** - (needed for contenarization). [Docker Installation Guide](https://docs.docker.com/desktop/install/)).

## data-engineering-structure
![alt text](Screenshot%20(282).png "DE structure overview")

The image above lays out the processing structure. We are going to go through an overview of why we try to adhere to this structure and will try to use the problem set above to explain how we are going to apply this structure to the problem set.

The first thing to note is our tech stack. We use PostgresSQL and local CSV file for data storage, our transformation logic to move data from A to B is not restricted to but normally carried out in Python or Spark (SQL).The orchestration of these tasks to run our full pipeline is managed by Airflow.

## Extract_Data

### Step 1
Create a config file with the following credentials below

```
[SOURCE]
currencies =  ['EGP','GHS','KES','MAD','NGN','UGX','XOF']
account_id = 'enter account_id'
api_key  =  'enter api key'

[DESTINATION]
schema = currency_exchange
POSTGRES_ADDRESS = localhost
POSTGRES_PORT = 5432
POSTGRES_USERNAME = postgres
POSTGRES_PASSWORD = 'enter DB password'
POSTGRES_DBNAME = autocheck
```

### Step 2
Create a Database on PostgreSQL with the name `autochek`  then We are going to write a simple script that pulls exchange rate from this (amazing) API [currencydata](https://www.xe.com/xecurrencydata/) 

We are just going to call the  `https://xecdapi.xe.com/v1/convert_to.json` and `https://xecdapi.xe.com/v1/convert_to.json`  API to grab a single currency exchange rate from target currency to USD and USD to target currency.
 

```
{'terms': 'http://www.xe.com/legal/dfs.php',
 'privacy': 'http://www.xe.com/privacy.php',
 'to': 'USD',
 'amount': 1.0,
 'timestamp': '2022-08-14T00:00:00Z',
 'from': [{'quotecurrency': 'NGN', 'mid': 419.2545920405}]}
```
 

So our function `get_exchange` in the script `extract.py` will call the two api and transform both api responses to a dictionary.The dictionary is then converted to a  `pandas dataframe`.


```
def get_exchange(currencies,account_id,api_key):

    """
        returns the exchange rate for a list of currncies from  https://www.xe.com/xecurrencydata/

        Parameters
        ----------
        currencies : List
            list of currencies to load

        account_id : str
           account id key
        
        api_key : str
            api key for a user's account
            
        Returns
            -------
            DataFrame 
                a dataframe containing the following columns timestamp , currency_from, USD_to_currency, currency_to_USD ,currency_to of the target currecies
    """

    all_currency_data = pd.DataFrame()
    #iterate over each currecy
    for currency in currencies:
        temp_data = {}
        params = (
            ('to', 'USD'),
            ('from', currency),
            ('amount', '1'),
        )
        # get the currency rate for  destination currency to 1 USD 
        from_response = requests.get("https://xecdapi.xe.com/v1/convert_to.json",auth = (account_id,api_key), params=params)
        # return the response in json format
        response1 = from_response.json()
        # get the currency rate for 1 USD to destination currency 
        to_response = requests.get("https://xecdapi.xe.com/v1/convert_from.json",auth = (account_id,api_key), params=params)
        # return the response in json format
        response2 = to_response.json()

        # mapping response to a dictionary 
        temp_data['timestamp'] = response2['timestamp']
        temp_data['currency_from'] = response2['to'][0]['quotecurrency']
        temp_data['USD_to_currency'] = response2['to'][0]['mid']
        temp_data['currency_to_USD'] = response1['from'][0]['mid']
        temp_data['currency_to'] = response1['from'][0]['quotecurrency']
        # converting the dictionary record to a dataframe
        single_currency_data = pd.DataFrame([temp_data])
        # appeding each currency record the universal currency dataframe 
        all_currency_data = pd.concat([all_currency_data,single_currency_data],axis = 0)
    #return the currency exchange
    return all_currency_data
```

The sample output looks like this .

![alt text](Screenshot%20(283).png "DataFrame output")


## Load_Data
we are going to load the returned dataframe to a local drive and a postgreSQL DB. our scipt will call the `load_to_local` function the `load.py` save a locally without duplicateds for each day

```
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
        historical_data =  pd.read_csv('historical_data.csv')
    except :
        historical_data = pd.DataFrame(columns=['timestamp' , 'currency_from', 'USD_to_currency', 'currency_to_USD' ,'currency_to'])
    
    #append new records to historical data
    historical_data = pd.concat([historical_data,data],axis= 0)
    historical_data = historical_data.reset_index(drop =  True)

    # drop duplicates if records are entered the same day
    historical_data = historical_data.drop_duplicates(subset=['timestamp' ,'currency_to'],keep = 'first')

    # overwrite existing transaction 
    historical_data.to_csv('historical_data.csv',index = False)

```

Also we call the `upsert_database` function in the `load.py` module to save to a postgreSQL DB.

```
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
    
```

here is a sample database output

![alt text](db_output.png "db_output") 


#### STEPS
   - Include necessary database parameters in the [CONFIG](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/config.ini) file.       POSTGRES_ADDRESS is the IP of the server dockers is running.  
   - Startup the [Postgres](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/docker-compose.yml) docker container. 
    
          docker-compose up
    
   - Execute the [etl.py]([https://github.com/JamiuAfolabi/autochek/blob/main/question_one/main.py](https://github.com/JamiuAfolabi/autochek/blob/main/question_two/dags/etl.py)) script. This script 
        - Create a DB Connection
        - Extract Exchange rate from API
        - Create a csv file and ingest data into it
        - Creates DB table and ingest the data
        


