from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from etl import etl_pipeline

default_args = {
    "retries": 5,
    "retry_delay": timedelta(minutes=1),
    "owner": "admin"
}

with DAG(dag_id="twitter_pieline",
        description="Extracting tweets and storing them in a database",
        start_date=datetime(2022, 12, 11, 12),
        schedule="*/20 * * * *"
        ) as dag:
    
    t1 = PythonOperator(
        task_id="print_tweets",
        python_callable=etl_pipeline
        )
    
    t1
