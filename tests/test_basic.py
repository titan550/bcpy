import bcpy
import numpy as np
import pandas as pd


def test_basic():
    assert bcpy.name == 'bcpy'


def test_format_file():
    df = pd.DataFrame(np.random.randint(-100, 100, size=(100, 4)), columns=list('ABCD'))
    assert bcpy.FormatFile.build_format_file(df) == '<BCPFORMAT xmlns="https://schemas.microsoft.com/sqlserver/2004/bulkload/format" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><RECORD><FIELD ID="1" xsi:type="CharTerm" TERMINATOR="," MAX_LENGTH="MAX" COLLATION="SQL_Latin1_General_CP1_CI_AS"/><FIELD ID="2" xsi:type="CharTerm" TERMINATOR="," MAX_LENGTH="MAX" COLLATION="SQL_Latin1_General_CP1_CI_AS"/><FIELD ID="3" xsi:type="CharTerm" TERMINATOR="," MAX_LENGTH="MAX" COLLATION="SQL_Latin1_General_CP1_CI_AS"/><FIELD ID="4" xsi:type="CharTerm" TERMINATOR="," MAX_LENGTH="MAX" COLLATION="SQL_Latin1_General_CP1_CI_AS"/></RECORD><ROW><COLUMN SOURCE="1" NAME="A" xsi:type="SQLNVARCHAR"/><COLUMN SOURCE="2" NAME="B" xsi:type="SQLNVARCHAR"/><COLUMN SOURCE="3" NAME="C" xsi:type="SQLNVARCHAR"/><COLUMN SOURCE="4" NAME="D" xsi:type="SQLNVARCHAR"/></ROW></BCPFORMAT>'


def test_import():
    df = pd.DataFrame(np.random.randint(-100, 100, size=(100, 4)), columns=list('ABCD'))
    bcpy.to_sql(df, sql_info={
        'server': 'localhost',
        'database': 'test_db',
        'schema': 'dbo',
        'table_name': 'test_table'
    })