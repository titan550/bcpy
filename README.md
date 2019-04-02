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
    <img src="https://img.shields.io/travis/titan550/bcpy/master.svg" alt="travis build status" />
    </a>
  </td>
</tr>
</table>

## Status

Under development and still does not work. Please check back later.

## What is it?

This package is a wrapper for Microsoft's SQL Server bcp utility. Current database drivers available in Python are not fast enough for transferring millions of records (yes, I have tried [pyodbc fast_execute_many](https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany)). Despite the IO hits, the fastest option by far is saving the data to a CSV file in file system (preferably /dev/shm tmpfs) and using the bcp utility to transfer the CSV file to SQL Server.

## Requirements

You need a working version of Microsoft bcp installed in your system. Your PATH environment variable should contain the directory of the bcp utility. Following are the installation tutorials for different operating systems.

- [Install bcp on Linux](https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-setup-tools)
- [Install bcp on Windows](https://docs.microsoft.com/en-us/sql/tools/bcp-utility)
