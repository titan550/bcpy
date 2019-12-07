import bcpy
import os


def test_flat_file_to_sql():
    sql_config = {
        'server': 'mssql',
        'database': 'bcpy',
        'username': 'SA',
        'table': 'test',
        'password': os.environ['MSSQL_SA_PASSWORD']
    }
    sql_table_name = 'test_data1'
    schema = 'my_test_schema'
    csv_file_path = 'tests/data1.csv'
    c = bcpy.FlatFile(qualifier='', path=csv_file_path)
    sql_table = bcpy.SqlTable(
        sql_config,
        table=sql_table_name,
        schema_name=schema)

    c.to_sql(sql_table)
    sql_server = bcpy.SqlServer(sql_config)
    count_from_sql = sql_server.run(
        f"select count(*) from {schema}.{sql_table_name}").iloc[0][0]
    with open(csv_file_path) as f:
        for i, _ in enumerate(f, 1):
            pass
        count_from_file = i - 1  # Subtracting one line because of header
    assert count_from_file == count_from_sql
