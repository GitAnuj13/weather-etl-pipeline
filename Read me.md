# Weather ETL Pipeline using Python, SQL Server and Flask

## Project Overview

This project demonstrates an end-to-end ETL (Extract, Transform, Load) pipeline using Python, SQL Server, and Flask.

The pipeline extracts weather data from the Open-Meteo API, transforms the data using Pandas, performs incremental loading based on Observation Time, stores the data in SQL Server, and displays the results through a Flask web application.

## Technologies Used

* Python
* Pandas
* Requests
* SQL Server
* PyODBC
* Flask
* Git & GitHub

## ETL Workflow

Weather API → Extract → Transform → Incremental Load → SQL Server → Flask Dashboard

## Features

* Weather data extraction from API
* Data transformation and cleansing
* Incremental loading logic
* SQL Server integration
* Logging and error handling
* Flask web application
* Dashboard displaying latest weather records

## Database Design

Table: fact_weather

Columns:

* WeatherID
* ObservationTime
* Temperature
* WindSpeed
* City
* LoadTimestamp

## Key Learnings

* ETL Architecture
* Incremental Loading
* Business Timestamp vs Load Timestamp
* SQL Server Integration
* Logging in ETL Pipelines
* Flask Application Development
* GitHub Version Control

## Author

Anuj Upadhyay
