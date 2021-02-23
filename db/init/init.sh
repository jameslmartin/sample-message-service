#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE messages_dev;
    GRANT ALL PRIVILEGES ON DATABASE messages_dev TO postgres;
EOSQL
