
# Base image
FROM apache/airflow:2.8.0-python3.11

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow

# Install system dependencies and Python libraries
USER root
RUN apt-get update && apt-get install -y \
    python3-pip \
    gcc \
    git \
    libpq-dev \
    && pip install --upgrade pip

# Install required Python packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy DAGs, scripts, and Flask app into the container
COPY ./shared /opt/airflow/shared
COPY api_app.py /opt/airflow/api_app.py

# Set working directory to Airflow home
WORKDIR /opt/airflow

# Expose ports for Flask and Airflow Web UI
EXPOSE 5000 8080

# Entrypoint for both services using supervisord
CMD ["bash", "-c", "airflow db init && \
    airflow users create -r Admin -u admin -p admin -e admin@example.com -f Admin -l User && \
    airflow scheduler & airflow webserver & python /opt/airflow/api_app.py"]
