#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE ROLE ${DATAPUSHER_DATASTORE_DB_USER} LOGIN PASSWORD '${DATAPUSHER_DATASTORE_DB_PASSWORD}';
    CREATE DATABASE ${DATAPUSHER_DATASTORE_DB_NAME} OWNER ${DATAPUSHER_DATASTORE_DB_USER} ENCODING 'utf-8';
    CREATE ROLE ${DATAPUSHER_JOBS_DB_USER} LOGIN PASSWORD '${DATAPUSHER_JOBS_DB_PASSWORD}';
    CREATE DATABASE ${DATAPUSHER_JOBS_DB_NAME} OWNER ${DATAPUSHER_JOBS_DB_USER} ENCODING 'utf-8';
    GRANT CREATE, CONNECT, TEMPORARY ON DATABASE ${DATAPUSHER_DATASTORE_DB_NAME} TO ${DATAPUSHER_DATASTORE_DB_USER};
    GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA public TO ${DATAPUSHER_DATASTORE_DB_USER};
EOSQL