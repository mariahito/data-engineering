# Data Engineering Final Project

## Team Members
- Zinia Mahabub
- Maria Jose Hito Ramos
- Tori-Ann Holness
- Tonya Sosa

## Overview
This project explores potential correlations between weather patterns, COVID-19 case surges, and unemployment rates across ten U.S. states during 2021. It demonstrates an end-to-end data pipeline that extracts, transforms, and loads datasets from CSV files and APIs, stores the data in a relational database, and serves insights through a Flask-based API.

## Technologies Used
- Python (Pandas, NumPy)
- Flask (for the API)
- PostgreSQL (relational database)
- Apache Airflow (for ETL automation)
- Docker (containerization)
- Jupyter Notebooks (for exploration)
- Excel/CSV/JSON (data formats)

## Dataset Sources
1. **COVID-19**: Johns Hopkins CSSE (historical confirmed cases)
2. **Unemployment**: U.S. Bureau of Labor Statistics (state-level monthly rates)
3. **Weather**: API (daily temperature, humidity, and precipitation data)

## Directory Structure
```
├── cleaned_covid.xlsx
├── cleaned_unemployment_data.csv
├── cleaned_weather_data.csv
├── combined_data.csv
├── clean_data_sql_merge.py
├── weather_data_retrievedfromAPI.py
├── api_app.py
├── etl_pipeline_dag.py
├── api_request.py
├── normalized_schema.sql
├── erd_diagram_script.py
├── Dockerfile
├── docker-compose.yml
├── erd_diagram.pdf
├── requirements.txt
├── config.json
├── FinalProjectDocumentation.pdf
```

## Setup Instructions

### 1. Run with Docker
```bash
docker-compose up --build
```

- Airflow UI: [http://localhost:8081](http://localhost:8081)
- Flask API: [http://localhost:5000](http://localhost:5000)

Use Airflow to trigger the `etl_project_pipeline` DAG to create `combined_data.csv`.

### 2. Manually Run
```bash
python api_app.py
```

## API Endpoints
- `/`: Welcome message
- `/cases-by-state`: COVID-19 case totals per state
- `/avg-unemployment-by-state`: Average unemployment rates
- `/avg-temp-by-state`: Average temperatures
- `/filter?state=XX&month=MM/YYYY`: Filter data by state and month

## ERD
See `erd_diagram.pdf` for the relational schema used to store cleaned data.
