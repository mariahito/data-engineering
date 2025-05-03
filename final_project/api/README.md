This portion of the project includes the **API** and **automation pipeline** as required in the final project instructions.

---

## Files Included

### 1. `api_app.py`
- Flask-based API that allows users to query and view aggregated weather and employment data.
- Endpoints:
  - `/` – Welcome message
  - `/avg-temp-by-state` – Returns average temperature grouped by state
  - `/unemployment-rate-by-month` – Returns average unemployment rate by month
  - `/filter-by-state?state=Texas` – Filters all records by a specific state
  - `/emp-pop-ratio` – Calculates and returns employment-to-population ratio by state

### 2. `transform_merge.py`
- Simulates the transformation and merging of raw datasets (COVID, weather, employment).
- Produces the final `combined_data.csv` file used by the API and database.

### 3. `etl_project_pipeline_dag.py`
- Apache Airflow DAG that automates the ETL process by running the transformation script.
- DAG Name: `etl_project_pipeline`
- Trigger manually from the Airflow UI.

### 4. `Dockerfile`
- Builds a Docker image that runs both:
  - Apache Airflow (Scheduler + Web UI)
  - Flask API
- Exposes ports:
  - `8080` → Airflow
  - `5000` → Flask API

---

## How to Run

### 1. Build and Start the Container
```bash
docker build -t final-project .
docker run -p 8080:8080 -p 5000:5000 final-project
```

### 2. Access the Services
- Airflow UI → http://localhost:8080
- Flask API → http://localhost:5000

### 3. Trigger the DAG
- Log into Airflow UI (user: `admin`, pass: `admin`)
- Enable and trigger the `etl_project_pipeline` DAG