#!/bin/bash

export PGPASSWORD=postgres
psql -U postgres -c "DROP DATABASE test_app"
psql -U postgres -c "DROP DATABASE app"
