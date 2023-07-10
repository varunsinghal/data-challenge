# Data Engineer Challenge

<br>

### Installation
- docker
- docker-compose
- bash (optional)


### Setup
* build the project
  ```bash
  $ make start
  ```
* initialize the database
  ```bash 
  $ make init_db
  ```
* add calendar years
  ```bash
  $ make calendar start=2018 end=2023
  ```


### Ingestion script
* customer.csv
  ```bash
  $ make customer FILE=/app/resources/customer.csv
  ```

* transaction.csv
  ```bash
  $ make transaction FILE=/app/resources/transaction.csv
  ```

* exchange_rate.csv
  ```bash
  $ make exchange_rate FILE=/app/resources/exchange_rate.csv
  ```

<br>
<br>


### Information System Architecture
**_Design a Data Flow architecture_**

![Data Flow architecture](/resources/data%20flow.png)


**_Which technologies do you propose? What are the advantages and disadvantages of those?_**

* API - to receive request from other platforms and enable a point of receiving the trigger. The API code has access to meta data tables, which can show the progress of the data journey - ingestion, validation, transformation, and extraction. 
* Meta data storage - to store the data of the request received to ingest/export data. It can also capture some key attributes from each request received to derive insights at later stages. It will enable logging of the data received and overrides (versioning) if requested.
* SQS/RabbitMQ - Any queue mechanism, where API will register the request to be picked up based upon the availability of the processor.
* Processor - Key engine which will listen to traffic being received in the SQS/RabbitMQ and will spawn a necessary process to execute it.
* Python script 
  * Loader - this will be request specific and will expand to incorporate more data source types like Salesforce, Kafka, S3, direct upload, other databases, etc.
  * Staging - this layer is responsible to hold the raw data in as is form.
  * Pipeline - basically set of queries - written to validate, clean, and transform data to ingest it into facts, dimensions and lookup tables.
* Views - these are virtual tables which abstract the necessary joins, and aggregations for the access of data via tableau or other BI tools.

<br>

### Data Modelling

**_Design a relational data model to represent the given datasets. It should be optimized for analytical purposes._**

![ER diagram](/resources/er-diagram.png)
file name: /sql/db_setup.sql

**_Explain the modeling approach taken. Is there any alternative to the model chosen (trade-offs, limitations, advantages)?_**

I took approach of snowflake schema - where I introduced 2 fact tables to store exchange rate and transaction data. Also, dimensions are introduced:
* dim_country - to store distinct country records
* dim_currency - to store distinct currency 
* dim_calendar - indexed table with date, month, and year columns
* dim_customer - to store distinct customers and reference it in fact tables.

A lookup table (map_country_currency) is also introduced to store the dependency between country and currency using the outgoing transaction data (per customer).

* Tradeoffs: 
  * query complexity - since data is normalized, so would need some joins to fetch data
  * join overhead - due to which, proper indexing and query optimization is essential.
* Limitations:
  * transformations required for ingestion of data.
  * validations/updates to be in place of dimension table - to be able to ingest the data.
* Advantages:
  * reduced data redundancy - created dimension data for the redundant data.
  * improved data consistency - better control of updates on the dimension data.


**_Propose a primary key implementation for each table, elaborating on the solution adopted._**

* dim_country - country_id 
* dim_currency - currency_id 
* map_country_currency - map_country_currency_id
* dim_calendar - date_id 
* dim_customer - customer_id 
* fact_transaction - transaction_id 
* fact_exchange_rate - exchange_rate_id 

<br>

### Python
**_Explain why your code is performant or how it can be improved._**

I am using a staging table to ingest data as is, and then validating the data in the database. This allows me to scale the queries in the database, because the validation is done in the staging table, and then only the validated data is loaded into the production schema. \
This helps in making the code performant, by allowing me to perform validation and transformation on the staging table (ELT approach).

<br>

### SQL
* Create a view which shows the total amount in EUR, number of transactions and number of unique users per month and country.\
  view name: `transaction_summary_view`\
  file name: `/sql/db_setup.sql` 

* Based on a date, show the evolution of the exchange rate for each currency (based on GBP) in percentage for the next 15 days \
  view name: `exchange_rate_view` \
  file name: `/sql/db_setup.sql` 
  
