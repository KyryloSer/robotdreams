-- Connect to the airflow database for remaining operations
\c ${POSTGRES__DB};

-- Create read-only user (safe if re-run)
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '${AIRFLOW_READONLY_USER}') THEN
    CREATE USER ${AIRFLOW_READONLY_USER} WITH PASSWORD '${AIRFLOW_READONLY_PASSWORD}';
  END IF;
END $$;

-- Allow read-only user to connect
GRANT CONNECT ON DATABASE ${POSTGRES_DB} TO ${AIRFLOW_READONLY_USER};

-- Airflow will create tables itself. Give read-only access to future tables/sequences created by airflowuser.
ALTER DEFAULT PRIVILEGES FOR USER ${POSTGRES_AIRFLOW_USER}
GRANT SELECT ON TABLES TO ${AIRFLOW_READONLY_USER};

ALTER DEFAULT PRIVILEGES FOR USER ${POSTGRES_AIRFLOW_USER}
GRANT SELECT ON SEQUENCES TO ${AIRFLOW_READONLY_USER};

-- (Optional) you can also grant USAGE on schema public (usually already granted)
GRANT USAGE ON SCHEMA public TO ${AIRFLOW_READONLY_USER};

-- Create a view to check Airflow DAG runs
/*CREATE OR REPLACE VIEW airflow_status AS
SELECT
    dag_id,
    execution_date,
    state,
    start_date,
    end_date
FROM
    dag_run
ORDER BY
    execution_date DESC;

-- Grant access to the view
GRANT SELECT ON airflow_status TO ${AIRFLOW_READONLY_USER}; */