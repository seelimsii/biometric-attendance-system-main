#!/bin/bash

echo "========================="
echo "   Check if var exists   "
echo "========================="
if [ -z "$MSSQL_SA_PASSWORD" ]; then
    echo "MSSQL_SA_PASSWORD environment variable is not set"
    exit 1
fi

echo "========================="
echo "      Create database    "
echo "========================="
/opt/mssql-tools/bin/sqlcmd \
    -S localhost \
    -U SA \
    -P "$MSSQL_SA_PASSWORD" \
    -Q "CREATE DATABASE etimetracklite
    ON (FILENAME = '/var/opt/mssql/data/${MSSQL_DB_NAME}.mdf'),
    (FILENAME = '/var/opt/mssql/log/${MSSQL_DB_NAME}.ldf')
    FOR ATTACH;"