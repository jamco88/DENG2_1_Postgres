# Udacity Data Engineering Nanodegree Project 2/1: Relational Database Modelling with Postgres

The aim of this project is to design and implement a Star Schema for a music streaming website, "sparkify". This database needs to be optimized for queries - allowing the applications owners to understand how their users interact with their application.

## ETL Pipeline

The raw data is saved in 2 JSON files. 

The first is saved in data/song_data - this is processed and fed into the artists and songs tables.

The second json file is saved in data/log_data - this is fed into both the time and users tables.

Each of these tables is now neatly normalised.


## Star Schema 

The schema requires us to create a Fact Table, Songplays, which draws on data from all four tables.


## Workflow / File Explanation

Template code provided by Udacity.
I worked through the etl.ipynb notebook, completing each block as assigned, and using the provided test notebook to check that the database was being written to correctly. Once this was completed, the pipeline was run in its entirety via etl.py.
create_tables.py = creates the tables
sql_queries.py = Creates, Inserts, Drops and Deletes the tables.

## How to run

From your terminal, type "python create_tables.py" then "python etl.py".



