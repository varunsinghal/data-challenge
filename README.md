
### Installations
- docker
- docker-compose
- bash (optional)

### Setup
build the project 
```
$ make start
```

initialize the database
```bash 
$ make init_db
```

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

