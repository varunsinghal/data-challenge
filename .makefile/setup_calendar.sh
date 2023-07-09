#!/bin/bash

startYear=$1
endYear=$2

export PGPASSWORD=postgres

for targetYear in $(seq $startYear $endYear); do
    # Check if the target year already exists in the table
    existing_year=$(psql -U postgres -d app -t -c "SELECT 1 FROM dim_calendar WHERE year = $targetYear LIMIT 1")

    # If the existing_year variable is not empty, exit the script
    if [[ -n "$existing_year" ]]; then
        echo "Records for the target year $targetYear already exist in the table. Skipping the year."
    else 
        psql -U postgres -d app -v targetYear=$targetYear -f /app/sql/add_calendar_year.sql
    fi
done
