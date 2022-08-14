# autochek

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

### IMPLEMENTATION WITH PYTHON

    This approach involves executing all logic of the code in python. The bulk of the transformation was carried out in pandas.
    It comes with ease developing a production ready code at a fast pace.
    
    However, this is not suitabl for very large datasets due to memory constraint and its inability to support multiprocessing.
    
    A notebook implementation is included
    
 
    
   [Notebook implementation](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/python_solution_two.ipynb)
   
   The [Result](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/output2.csv) was generated as a CSV.


### IMPLEMENTATION WITH PYTHON AND SQL


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
 

### IMPLEMENTATION WITH PYSPARK
  - This method is highly efficient when integrated with HDFS. This should be considered when the dataset is very large. It supports Multiprocessing,
    hence, increasing the speed of transformation


