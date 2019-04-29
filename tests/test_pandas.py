import bcpy
import pandas as pd
import numpy as np
import os


def test_import():
    df = pd.DataFrame(np.random.randint(-100, 100, size=(100, 4)), columns=list('ABCD'))
    bdf = bcpy.DataFrame(df)
    sql = bcpy.SqlTable({
        'server': 'mssql',
        'database': 'bcpy',
        'table': 'test_dataframe',
        'username': 'SA',
        'password': os.environ['MSSQL_SA_PASSWORD']
    })
    bdf.to_sql(sql)