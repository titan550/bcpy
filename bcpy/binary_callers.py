import subprocess
import pandas as pd
from io import StringIO


def bcp(sql_table, flat_file):
    if sql_table.with_krb_auth:
        auth = ['-T']
    else:
        auth = ['-U', sql_table.username, '-P', sql_table.password]
    full_table_string = \
        f'{sql_table.database}.{sql_table.schema}.{sql_table.table}'
    bcp_command = ['bcp', full_table_string, 'IN', flat_file.path, '-f',
                   flat_file.get_format_file_path(), '-S',
                   sql_table.server] + auth
    if flat_file.file_has_header_line:
        bcp_command += ['-F', '2']
    result = subprocess.run(bcp_command)
    if result.returncode:
        raise Exception(f'Bcp command failed. Details:\n{result}')


def sqlcmd(server, database, command, username=None, password=None):
    if not username or not password:
        auth = ['-T']
    else:
        auth = ['-U', username, '-P', password]
    command = 'set nocount on;' + command
    sqlcmd_command = ['sqlcmd', '-S', server, '-d', database, '-b'] + auth + \
                     ['-s,', '-W', '-Q', command]
    result = subprocess.run(sqlcmd_command, stdout=subprocess.PIPE)
    if result.returncode:
        print(result.stdout)
        raise Exception(f'Sqlcmd command failed. Details:\n{result}')
    output = StringIO(result.stdout.decode('ascii'))
    first_line_output = output.readline().strip()
    if first_line_output == '':
        print(first_line_output)
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
