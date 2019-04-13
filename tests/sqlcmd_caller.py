import subprocess
import os


def sqlcmd_caller(command_file_path):
    result = subprocess.run(['/opt/mssql-tools/bin/sqlcmd',
                    '-S', f'mssql',
                    '-U', 'SA',
                    '-P', os.environ['MSSQL_SA_PASSWORD'],
                    '-i', command_file_path])
    if result.returncode != 0:
        raise Exception(result.stderr) # TODO find out why stderr is empty
