from .sqlcmd_caller import sqlcmd_caller

# TODO: create docker-compose so that we can call mssql-server with dns name


def test_create_db():
    sqlcmd_caller('create_test_db.sql')


def test_create_table():
    sqlcmd_caller('create_test_table.sql')
