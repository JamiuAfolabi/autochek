# autochek
Pipeline to deliver task

### QUESTION ONE

This project was aimed at generating a transformed data for the business.

The data was studied and analyzed to get an overview of the project. Findings include:

  - Some dates were out of range, hence a function was designed to parse the dates.
  
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
    

### IMPLEMENTATION WITH PYTHON AND SQL

   This involves ingesting the data from the source to an SQL Database. This provides a memory store and processing power is shared
   by the driver node(system running the python script) and the database engine. It also provides a persistent store where other BI tools
   can easily integrate.
   
   An ETL pipeline was built to ingest data from Google Sheet to Postgres on Dockers Container
   
- IMPLEMENTATION WITH PYTHON
- Pyspark


