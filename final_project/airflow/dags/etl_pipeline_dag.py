from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

dag = DAG(
    dag_id='etl_pipeline_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='Run clean_data_merge_sql.py to load data, clean it, and load into db'
)

def run_clean_script():
    subprocess.run(["python3", "/home/jhu/python_scripts/clean_data_sql_merge.py"], check=True)

merge_task = PythonOperator(
    task_id='merge_cleaned_data',
    python_callable=run_clean_script,
    dag=dag
)
