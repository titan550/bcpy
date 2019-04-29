import subprocess


def bcp(sql_table, flat_file):
    if sql_table.with_krb_auth:
        auth = ['-T']
    else:
        auth = ['-U', sql_table.username, '-P', sql_table.password]
    full_table_string = f'{sql_table.database}.{sql_table.schema}.{sql_table.table}'
    bcp_command = ['bcp', full_table_string, 'IN', flat_file.path, '-f', flat_file.get_format_file_path(), '-S', sql_table.server] + auth
    if flat_file.file_has_header_line:
        bcp_command += ['-F', '2']
    result = subprocess.run(bcp_command)
    if result.returncode:
        raise Exception(result.stderr)


def sqlcmd(server, database, command, username=None, password=None):
    if not username or not password:
        auth = ['-T']
    else:
        auth = ['-U', username, '-P', password]
    sqlcmd_command = ['sqlcmd', '-S', '-d', database] + auth + ['-q', command]
    result = subprocess.run(sqlcmd_command)
    if result.returncode:
        raise Exception(result.stderr)