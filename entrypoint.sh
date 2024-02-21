#!/bin/bash

check_db() {
    until pg_isready -h exch-db -p 5432; do
        echo "Waiting for database to become available..."
        sleep 1
    done
    echo "Database is available"
}

check_db

echo "Performing migrations"
alembic upgrade head

echo "Initializing data"
python setup.py

echo "Running uvicorn"
make start
