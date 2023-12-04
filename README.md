# Multinational Retail Data Centralisation
This data centralisation project is aimed at building a system that stores retail data coming from various sources (e.g. remote database, websites, API) into a local database, which then can be queried to obtain the desired metrics for business analyses.
The procedures in this project are grouped into 4 milestones which mainly consist of creating a local PostgreSQL database, data extraction and processing, building database schema and running SQL queries.

Key technologies used: Python, Pandas, Postgres SQL, AWS , API. 

# Usage Instructions
## Set up (milestone-1)
Setting up github and, python environment and local Postgres SQL database.  

## Running the scripts (miletsone-2 to milestone-4)
The steps to run this project are split into 3 milestones (milestone-2, milestone-3 and milestone-4). 
1. The first one (milestone-2) is running a python implementation which will extract the required data from different sources, process and clean them before uploading them to a local Postgre DB.
This is done by running [milestone2.py](https://github.com/antsia-github/multinational-retail-data-centralisation/blob/main/milestone2.py) script in the terminal :

```python
python milestone2.py  
```
It is not very clear, however, why the DataExtraction and DataCleaning classes are necessary (following project instructions) for the python implementation while function modules seem to fit better for the purpose.


2. The second step (milestone-3) is needed to make the uploaded data (from milestone-2) in the local Postgre DB fit as a relational database system. All the procedures in this milestone are bundled in a single SQL script [SQL/milestone3.sql](https://github.com/antsia-github/multinational-retail-data-centralisation/blob/main/SQL/milestone3.sql).
These can be performed by running the script using e.g. pgadmin4 or other supported IDE such as VS Code.

3. The final step (milestone-4) is getting some meaningful aggregate information from the SQL RDB (the outcome of milestone-3).
This consists of 9 tasks, each with its own SQL script (milestone4-task1.sql through to milestone4-task9.sql in [SQL](https://github.com/antsia-github/multinational-retail-data-centralisation/tree/main/SQL) directory) which can be executed using e.g. pgadmin4 or other supported IDE such as VS Code.

