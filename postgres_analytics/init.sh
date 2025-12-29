#!/bin/bash
set -e
echo "=== DEBUG: Postgres analytics init env ==="
echo "POSTGRES_USER = '$POSTGRES_USER'"
echo "POSTGRES_DB   = '$POSTGRES_DB'"
echo "================================"
# Replace environment variables in the SQL file
envsubst < /docker-entrypoint-initdb.d/init.sql.template > /tmp/init.sql

# Execute the processed SQL file
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f /tmp/init.sql