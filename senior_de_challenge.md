# Data Engineer Challenge

## Objective:

As a data engineer, you have been presented with a simulated dataset containing three files, namely **customers.csv, transactions.csv, and exchange_rate.csv**.\
\
Your objective for this evaluation is to demonstrate your proficiency in data engineering using Python and/or SQL.\
\
Your task involves examining the given datasets and load them into a data warehouse for further usage.\
\
The assessment will assess your ability to help stakeholders solving analytical problems using data modeling, as well as your proficiency in Python/SQL programming. Additionally, it's crucial that you ensure your code is well-commented and formatted to facilitate code clarity.

### Submission
* You have 4 days to complete the challenge. If you need additional time, please reach out before the deadline.
* Once you are done, please send your solution by email in a .zip file, 
* Please provide instructions for how to run the code (dependencies and requirements).
* You are free to make assumptions within tasks that may not be clear.


## Tasks:

### Information System Architecture
* Design a Data Flow architecture with the following requirements
  * The sources include Kafka topics, operational databases and csv files.
  * It follows the ELT approach.
  * Data is mainly accessible via Tableau.
* Which technologies do you propose? What are the advantages and disadvantages of those?

### Data Modelling
* Design a relational data model to represent the given datasets. It should be optimized for analytical purposes.
  * Consider best practices for historization.
  * Requirement: there is a dependancy between country of a customer and currency of an out-going transaction
* Explain the modeling approach taken. Is there any alternative to the model chosen (trade-offs, limitations, advantages)?
* Propose a primary key implementation for each table, elaborating on the solution adopted.

### Python
* Write python scripts (**avoid notebooks**) that loads the data into their respective tables based on your architecture and data model.
  * Ensure that data is cleaned, validated and deduplicated.
  * Generate additional data if neccessary.
* Add at least one python test.
* Add logging to the code to evaluate ingestion performance.
  * Explain why your code is performant or how it can be improved.
* The code should run without any modification from our side.
* Provide any specific versions, dependencies, libraries, etc. that we need to run the code.

### SQL
* Create a view which shows the total amount in EUR, number of transactions and number of unique users per month and country.
* Based on a date, show the evolution of the exchange rate for each currency (based on GBP) in percentage for the next 15 days


**Good luck!**
