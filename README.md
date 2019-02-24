# bcpy

This package is a wrapper for Microsoft's SQL Server bcp utility. Current database drivers available in Python are not fast enough for transferring millions of records (yes, I have tried [pyodbc fast_execute_many](https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany)). Despite the IO hits, the fastest option by far in saving the data to a CSV file in file system (preferably /dev/shm tmpfs) and using the bcp utility to transfer the CSV file to SQL Server.

## Requirements

You need a working version of Microsoft bcp installed in your system. Your PATH environment variable should contain the directory of the bcp utility. Following are the installation tutorials for different operating systems.

- [Install bcp on Linux](https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-setup-tools)
- [Install bcp on Windows](https://docs.microsoft.com/en-us/sql/tools/bcp-utility)