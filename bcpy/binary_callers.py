import subprocess
from io import StringIO
import hashlib

import pandas as pd


def sha512(text, encoding='utf-8'):
    """Converts an input string to its sha512 hash
    """
    if not isinstance(text, bytes):
        if isinstance(text, str):
            text = text.encode(encoding)
        else:
            raise ValueError('Invalid input. Cannot compute hash.')
    return hashlib.sha512(text).hexdigest()


def bcp(sql_table, flat_file, batch_size):
    """Runs the bcp command to transfer the input flat file to the input
    SQL Server table.
    :param sql_table: The destination Sql Server table
    :type sql_table: SqlTable
    :param flat_file: Source flat file
    :type flat_file: FlatFile
    :param batch_size: Batch size (chunk size) to send to SQL Server
    :type batch_size: int
    """
    if sql_table.with_krb_auth:
        auth = ['-T']
    else:
        auth = ['-U', sql_table.username, '-P', sql_table.password]
    full_table_string = \
        f'{sql_table.database}.{sql_table.schema}.{sql_table.table}'
    try:
        bcp_command = ['bcp', full_table_string, 'IN', flat_file.path, '-f',
                       flat_file.get_format_file_path(), '-S',
                       sql_table.server, '-b', str(batch_size)] + auth
    except Exception as e:
        args_clean = list()
        for arg in e.args:
            if isinstance(arg, str):
                arg = arg.replace(sql_table.password,
                                  sha512(sql_table.password))
            args_clean.append(arg)
        e.args = tuple(args_clean)
        raise e
    if flat_file.file_has_header_line:
        bcp_command += ['-F', '2']
    result = subprocess.run(bcp_command, stderr=subprocess.PIPE)
    if result.returncode:
        raise Exception(
            f'Bcp command failed. Details:\n{result}')


def sqlcmd(server, database, command, username=None, password=None, trusted_connection=False):
    """Runs the input command against the database and returns the output if it
     is a table.
    Leave username and password to None if you intend to use
    Kerberos integrated authentication
    :param server: SQL Server
    :type server: str
    :param database: Name of the default database for the script
    :type database: str
    :param command: SQL command to be executed against the server
    :type command: str
    :param username: Username to use for login
    :type username: str
    :param password: Password to use for login
    :type password: str
    :param trusted_connection: Use trusted connection
    :type trusted_connection: bool   
    :return: Returns a table if the command has an output. Returns None
             if the output does not return anything.
    :rtype: Pandas.DataFrame
    """
    if not username or not password:
        if trusted_connection:
            auth = ['-T']
        else:
            auth = ['-E']
    else:
        auth = ['-U', username, '-P', password]
    command = 'set nocount on;' + command
    sqlcmd_command = ['sqlcmd', '-S', server, '-d', database, '-b'] + auth + \
                     ['-s,', '-W', '-Q', command]
    result = subprocess.run(sqlcmd_command, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    if result.returncode:
        result_dump = str(result).replace(password, sha512(password))
        raise Exception(f'Sqlcmd command failed. Details:\n{result_dump}')
    output = StringIO(result.stdout.decode('ascii'))
    first_line_output = output.readline().strip()
    if first_line_output == '':
        header = None
    else:
        header = 'infer'
    output.seek(0)
    try:
        result = pd.read_csv(
            filepath_or_buffer=output,
            skiprows=[1],
            header=header)
    except pd.errors.EmptyDataError:
        result = None
    return result
