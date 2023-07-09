#!/bin/bash

export PGPASSWORD=postgres
psql -U postgres -c "CREATE DATABASE test_app"
psql -U postgres -c "CREATE DATABASE app"
psql -U postgres -d app -f /app/sql/db_setup.sql
