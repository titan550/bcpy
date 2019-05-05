#!/bin/bash
echo "Preparing the database before running pytest."
sqlcmd -S mssql -U SA -P $MSSQL_SA_PASSWORD -i tests/create_test_db.sql
pytest -v
