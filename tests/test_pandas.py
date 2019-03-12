import bcpy
import pandas as pd
import numpy as np


def test_import():
    df = pd.DataFrame(np.random.randint(-100, 100, size=(100, 4)), columns=list('ABCD'))
    bcpy.to_sql(df, sql_info={
        'server': 'localhost',
        'database': 'test_db',
        'schema': 'dbo',
        'table_name': 'test_table'
    })
