from .sqlcmd_caller import sqlcmd_caller


def test_create_db():
    sqlcmd_caller('tests/create_test_db.sql')


def test_create_table():
    sqlcmd_caller('tests/create_test_table.sql')
