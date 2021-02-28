#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE messages_dev;
    CREATE DATABASE messages_test;
    GRANT ALL PRIVILEGES ON DATABASE messages_dev TO postgres;
    GRANT ALL PRIVILEGES ON DATABASE messages_test TO postgres;
EOSQL
