# bcpy

<table>
<tr>
  <td>Latest Release</td>
  <td>
    <a href="https://pypi.org/project/bcpy/">
    <img src="https://img.shields.io/pypi/v/bcpy.svg" alt="latest release" />
    </a>
  </td>
</tr>
<tr>
  <td>License</td>
  <td>
    <a href="https://github.com/titan550/bcpy/blob/master/LICENSE">
    <img src="https://img.shields.io/pypi/l/bcpy.svg" alt="license" />
    </a>
</td>
</tr>
<tr>
  <td>Build Status (master)</td>
  <td>
    <a href="https://travis-ci.org/titan550/bcpy">
    <img src="https://api.travis-ci.org/titan550/bcpy.svg?branch=master" alt="travis build status" />
    </a>
  </td>
</tr>
</table>

## What is it?

This package is a wrapper for Microsoft's SQL Server bcp utility. Current database drivers available in Python are not fast enough for transferring millions of records (yes, I have tried [pyodbc fast_execute_many](https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany)). Despite the IO hits, the fastest option by far is saving the data to a CSV file in file system (preferably /dev/shm tmpfs) and using the bcp utility to transfer the CSV file to SQL Server.

## How Can I Install It?

You can download and install this package from PyPI repository by running the command below.

```bash
pip install bcpy
```

## Examples

Following examples show you how to load (1) flat files and (2) DataFrame objects to SQL Server using this package.

### Flat File

Following example assumes that you have a comma separated file with no qualifier in path 'tests/data1.csv'. The code below sends the the file to SQL Server.

```python
import bcpy


sql_config = {
    'server': 'sql_server_hostname',
    'database': 'database_name',
    'username': 'test_user',
    'password': 'test_user_password1234'
}
sql_table_name = 'test_data1'
csv_file_path = 'tests/data1.csv'
flat_file = bcpy.FlatFile(qualifier='', path=csv_file_path)
sql_table = bcpy.SqlTable(sql_config, table=sql_table_name)
flat_file.to_sql(sql_table)
```

### DataFrame

The following example creates a DataFrame with 100 rows and 4 columns populated with random data and then it sends it to SQL Server.

```python
import bcpy
import numpy as np
import pandas as pd


sql_config = {
    'server': 'sql_server_hostname',
    'database': 'database_name',
    'username': 'test_user',
    'password': 'test_user_password1234'
}
table_name = 'test_dataframe'
df = pd.DataFrame(np.random.randint(-100, 100, size=(100, 4)),
                  columns=list('ABCD'))
bdf = bcpy.DataFrame(df)
sql_table = bcpy.SqlTable(sql_config, table=table_name)
bdf.to_sql(sql_table)
```

## Requirements

You need a working version of Microsoft bcp installed in your system. Your PATH environment variable should contain the directory of the bcp utility. Following are the installation tutorials for different operating systems.

- [Dockerfile (Ubuntu 18.04)](./bcp.Dockerfile)
- [Linux](https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-setup-tools)
- [Mac](https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-setup-tools?view=sql-server-2017#macos)
- [Windows](https://docs.microsoft.com/en-us/sql/tools/bcp-utility)
