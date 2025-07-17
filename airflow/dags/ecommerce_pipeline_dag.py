from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add path to access the scripts folder inside Docker
sys.path.append("/opt/airflow/scripts")

# Import the functions to be used in the DAG
from ingest import ingest_data
from clean import clean_data
from process import process_data
from train_model import train_model
from report import generate_report

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(seconds=30),
}

with DAG(
    dag_id="ecommerce_pipeline",
    max_active_runs=1, 
    default_args=default_args,
    description="E-commerce forecasting pipeline using MongoDB and Prophet",
    schedule_interval="@daily",  # daily batch ingestion
    catchup=False,
    tags=["ecommerce", "forecasting", "prophet"],
) as dag:

    # Step 1: Ingest raw CSV into MongoDB
    ingest = PythonOperator(task_id="ingest_data", python_callable=ingest_data)

    # Step 2: Clean and filter raw collection → clean collection
    clean = PythonOperator(task_id="clean_data", python_callable=clean_data)

    # Step 3: Aggregate daily sales from clean collection
    process = PythonOperator(task_id="process_data",
                             python_callable=process_data)

    # Step 4: Train Prophet model on time-series data
    train = PythonOperator(task_id="train_model",
                           python_callable=train_model)

    # Step 5: Write predictions to CSV for Flask app
    report = PythonOperator(task_id="generate_report",
                            python_callable=generate_report)

    # Define task dependencies
    ingest >> clean >> process >> train >> report
