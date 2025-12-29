from __future__ import annotations

from datetime import datetime
from pathlib import Path
import pytz

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from python_scripts.train_model import process_iris_data


DAGS_DIR = Path(__file__).resolve().parent
DBT_ROOT = DAGS_DIR / "dbt"
DBT_PROJECT_DIR = DBT_ROOT / "homework"
DBT_PROFILES_DIR = DBT_ROOT

kyiv_tz = pytz.timezone("Europe/Kiev")

default_args = {
    "owner": "airflow",
    "retries": 0,
}

with DAG(
    dag_id="process_iris",
    default_args=default_args,
    description="Process Iris with dbt and train ML model",
    start_date=datetime(2025, 4, 22, 1, 0, tzinfo=kyiv_tz),
    end_date=datetime(2025, 4, 24, 1, 0, tzinfo=kyiv_tz),
    schedule="0 1 * * *",
    catchup=True,
    max_active_runs=1,
    tags=["homework", "dbt", "ml"],
) as dag:

    dbt_transform_iris = BashOperator(
        task_id="dbt_transform_iris",
        bash_command=(
            "dbt run "
            "--project-dir '{{ params.project_dir }}' "
            "--profiles-dir '{{ params.profiles_dir }}' "
            "--select iris_processed "
            "--vars '{\"process_date\": \"{{ ds }}\"}'"
        ),
        params={
            "project_dir": str(DBT_PROJECT_DIR),
            "profiles_dir": str(DBT_PROFILES_DIR),
        },
    )

    train_model = PythonOperator(
        task_id="train_model",
        python_callable=process_iris_data,
        provide_context=True,
    )

    dbt_transform_iris >> train_model