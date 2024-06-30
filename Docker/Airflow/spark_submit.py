from airflow import DAG
from datetime import datetime
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

with DAG('spark_submit_job', start_date=datetime(2022, 1, 1), schedule_interval='@daily') as dag:
    submit_job = SparkSubmitOperator(
        task_id = 'submit_job',
        application='/include/sparksubmit_productevent.py',
        conn_id='spark_test',
        total_executor_cores='1',
        executor_cores='1',
        executor_memory='1g',
        num_executors='1',
        driver_memory='1g',
        verbose=False
    )

