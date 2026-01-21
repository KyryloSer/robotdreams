from __future__ import annotations

from datetime import datetime
import os
from pathlib import Path
import pytz

from airflow import DAG
from dbt_operator import DbtOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

from python_scripts.train_model import process_iris_data


DAGS_DIR = Path(__file__).resolve().parent
DBT_ROOT = DAGS_DIR / "dbt"
DBT_PROJECT_DIR = DBT_ROOT / "homework"
DBT_PROFILES_DIR = DBT_ROOT
DBT_PROFILE = "homework"
KYIV_TZ = pytz.timezone("Europe/Kiev")

default_args = {
    "owner": "airflow",
    "retries": 0,
}

env_vars = {
    "ANALYTICS_DB": os.getenv("ANALYTICS_DB", "analytics"),
    "DBT_PROFILE": DBT_PROFILE,
}

dbt_vars = {
    "is_test": False,
    "data_date": "{{ ds }}",
}

with DAG(
    dag_id="process_iris",
    default_args=default_args,
    description="Process Iris with dbt and train ML model",
    start_date=datetime(2025, 4, 22, 0, 0, tzinfo=KYIV_TZ),
    end_date=datetime(2025, 4, 24, 23, 59, tzinfo=KYIV_TZ),
    schedule="0 1 * * *",
    catchup=True,
    max_active_runs=1,
    tags=["homework", "dbt", "ml"],
) as dag:

    dbt_seed_iris = DbtOperator(
        task_id="dbt_seed_iris",
        command="seed",
        profile=DBT_PROFILE,
        project_dir=DBT_PROJECT_DIR,
        env_vars=env_vars,
        vars=dbt_vars,
    )

    dbt_run_iris = DbtOperator(
        task_id="dbt_run_iris",
        command="run",
        profile=DBT_PROFILE,
        project_dir=DBT_PROJECT_DIR,
        env_vars=env_vars,
        vars=dbt_vars,
    )

    dbt_test_iris = DbtOperator(
        task_id="dbt_test_iris",
        command="test",
        profile=DBT_PROFILE,
        project_dir=DBT_PROJECT_DIR,
        fail_fast=True,
        env_vars=env_vars,
        vars=dbt_vars,
    )

    train_model = PythonOperator(
        task_id="train_model",
        python_callable=process_iris_data,
        op_kwargs={"process_date": "{{ ds }}"},
    )

    # email
    notify_success = EmptyOperator(task_id="notify_success")

    dbt_seed_iris >> dbt_run_iris >> dbt_test_iris >> train_model >> notify_success