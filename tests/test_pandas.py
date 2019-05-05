import os

import numpy as np
import pandas as pd

import bcpy


def test_import():
    sql_config = {
        'server': 'mssql',
        'database': 'bcpy',
        'username': 'SA',
        'password': os.environ['MSSQL_SA_PASSWORD']
    }
    table_name = 'test_dataframe'
    df = pd.DataFrame(np.random.randint(-100, 100, size=(100, 4)),
                      columns=list('ABCD'))
    bdf = bcpy.DataFrame(df)
    sql_table = bcpy.SqlTable(sql_config, table=table_name)
    bdf.to_sql(sql_table)
    sql_server = bcpy.SqlServer(sql_config)
    sum_of_column_d_from_sql = \
        sql_server.run(
            f"select sum(cast(D as int)) from {table_name}").iloc[0][0]
    assert sum_of_column_d_from_sql == df['D'].sum()
