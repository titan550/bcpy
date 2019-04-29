# coding: utf-8
import bcpy
import os


c = bcpy.FlatFile(qualifier='', path='tests/data1.csv')
sql = sql = bcpy.SqlTable({
    'server': 'mssql',
    'database': 'bcpy',
    'table': 'test_data1',
    'username': 'SA',
    'password': os.environ['MSSQL_SA_PASSWORD']
})
c.to_sql(sql)
