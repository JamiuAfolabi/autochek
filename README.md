# autochek
Pipeline to deliver task

### QUESTION ONE

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
   - Startup the [Postgres](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/docker-compose.yml) docker container. 
    
          docker-compose up
   - Include necessary database parameters in the [CONFIG](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/config.ini) file   
   - Execute the [Main.py](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/main.py) script. This script 
        - Create [DB Connection](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/dbconnection.py)
        - [Transform](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/parse.py) the data parsed
        - Creates table using [Relationship.sql](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/relationship.sql) and ingest the data
        - Execute [Result.sql](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/result.sql) script to generate the desired output
        - Save the result in [Output.csv](https://github.com/JamiuAfolabi/autochek/blob/main/question_one/output.csv)
 

### IMPLEMENTATION WITH PYSPARK
  - This method is highly efficient when integrated with HDFS. This should be considered when the dataset is very large. It supports Multiprocessing,
    hence, increasing the speed of transformation


