import csv
import os

from .binary_callers import bcp, sqlcmd
from .format_file_builder import FormatFile
from .tmp_file import TemporaryFile


class DataObject:
    """Base object for data objects in bcpy
    """

    def __init__(self, config):
        if config and not isinstance(config, dict):
            raise TypeError('Config parameter must be a dictionary object')

    def __repr__(self):
        output = str()
        for attrib, value in self.__dict__.items():
            output += f'{attrib} = {repr(value)}\n'
        return output

    def __str__(self):
        return self.__repr__()


class FlatFile(DataObject):
    def __init__(self, config=None, **kwargs):
        """
        :param config: A dictionary object with the parameters.
        :param kwargs: Dynamic list of params which supersedes config params if
                       they overlap.
        :param delimiter: flat file delimiter (default: ",")
        :param qualifier: flat file qualifier
                          (default: "'" , e.g., 'col1','col2')

        :param newline: newline characters that separate records
                        (default: "\n")
        :param path: path to the flat file
        :param file_has_header_line: defaults to False
        :param columns: a list of columns, automatically read from the file
                        if the if the file has header a line.
        """
        super().__init__(config)
        self.delimiter = ','
        self.qualifier = '\''
        self.newline = '\n'
        self.__columns = None
        self.path = None
        self.__format_file_path = None
        self.file_has_header_line = False
        if config:
            for key, value in config.items():
                setattr(self, key, value)
        for key, value in kwargs.items():
            setattr(self, key, value)
        if not self.qualifier:
            self.qualifier = ''

    def __del__(self):
        """Removes the temporary format file that gets created before sending
        the flat file to SQL Server"""
        try:
            if self.__format_file_path:
                os.remove(self.__format_file_path)
        except AttributeError:
            pass

    def _read_columns_from_file(self):
        """Reads columns of a flat file from its file located in object's path
        attribute. Is stores the results in the object's columns attribute.

        Note: Caller of this method assumes that the file has headers.
        """
        with open(self.path, encoding='utf-8-sig') as f:
            header = f.readline()
        qualifier_delimiter_combo = str.format('{0}{1}{0}', self.qualifier,
                                               self.delimiter)
        columns_raw = header.split(qualifier_delimiter_combo)
        self.__columns = [columns_raw[0].lstrip(self.qualifier)]
        self.__columns.extend(columns_raw[1:-1])
        self.__columns.append(
            columns_raw[-1].rstrip(self.qualifier + self.newline))
        self.file_has_header_line = True

    def get_format_file_path(self, recalculate=False):
        """Returns the path to the bcp format file of the this flat file
        :param recalculate: uses file from cache if recalculate if False
                            otherwise it will remove the old file and creates a
                            new one.
        :return: path to the format file
        :rtype: str
        """
        if not recalculate and self.__format_file_path:
            return self.__format_file_path
        else:
            try:
                if self.__format_file_path:
                    os.remove(self.__format_file_path)
            except OSError:
                pass
        if not self.columns:
            raise Exception(
                'Need the object columns or path to build the format file')
        self.__format_file_path = self._build_format_file()
        return self.__format_file_path

    def _build_format_file(self):
        """Creates the format file and writes its content to a temporary file.
        :return: path to the temporary file
        :rtype: str
        """
        format_file_content = FormatFile.build_format_file(self)
        with TemporaryFile(mode='w') as f:
            f.write(format_file_content)
            format_file_path = f.name
        return format_file_path

    def _get_sql_create_statement(self, table_name=None):
        """Creates a SQL drop and re-create statement corresponding to the
        columns list of the object.

        :param table_name: name of the new table
        :type table_name: str
        :return: SQL code to create the table
        """
        if not table_name:
            table_name = os.path.basename(self.path)
        sql_cols = ','.join(
            map(lambda x: f'[{x}] nvarchar(max)', self.columns))
        sql_command = f"if object_id('[dbo].[{table_name}]', 'U') " \
            f"is not null drop table [dbo].[{table_name}];" \
            f'create table [dbo].[{table_name}] ({sql_cols});'
        return sql_command

    def to_sql(self, sql_table, use_existing_sql_table=False, batch_size=10000):
        """Sends the object to SQL table
        :param sql_table: destination SQL table
        :type sql_table: SqlTable
        :param use_existing_sql_table: If to use an existing table in the SQL database. 
        If not, then creates a new one.
        :type use_existing_sql_table: bool
        :param batch_size: Batch size (chunk size) to send to SQL Server
        :type batch_size: int
        """
        if not use_existing_sql_table:
            sqlcmd(
                server=sql_table.server,
                database=sql_table.database,
                command=self._get_sql_create_statement(table_name=sql_table.table),
                username=sql_table.username,
                password=sql_table.password)
        bcp(sql_table=sql_table, flat_file=self, batch_size=batch_size)

    @property
    def columns(self):
        if not self.__columns and self.path:
            self._read_columns_from_file()
        return self.__columns

    @columns.setter
    def columns(self, columns):
        if isinstance(columns, list):
            self.__columns = columns
        else:
            raise TypeError('Columns parameter must be a list of columns')


class SqlServer(DataObject):
    def __init__(self, config=None, **kwargs):
        """Leave the username and password to None to use Kerberos
        integrated authentication
        :param config: A dictionary object with the parameters.
        :param kwargs: Dynamic list of params which supersedes config params if
                       they overlap.
        :param database: default database to use for operations
        :param server: server name
        :param username: username for SQL login (default: None)
        :param password: password for SQL login (default: None)
        """
        # todo: make Sql Server one of the attributes of SqlTable
        super().__init__(config)
        self.database = 'master'
        self.server = 'localhost'
        self.username = None
        self.password = None
        if config:
            for key, value in config.items():
                setattr(self, key, value)
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def with_krb_auth(self):
        """Returns True if the object uses Kerberos for authentication.
        :return: Kerberos authentication eligibility
        :rtype: bool
        """
        if hasattr(self, 'username') and hasattr(self, 'password') and self.username and self.password:
            result = False
        else:
            result = True
        return result

    def run(self, command):
        """Runs the input command against the database and returns the
        result (if any).
        :param command: SQL statement to run.
        :type command: str
        :return: Table of results or None if the command does not return
        results
        :rtype: pandas.DataFrame
        """
        return sqlcmd(
            server=self.server,
            database=self.database,
            command=command,
            username=self.username,
            password=self.password)


class SqlTable(DataObject):
    def __init__(self, config=None, **kwargs):
        """Leave the username and password to None to use Kerberos
        integrated authentication
        :param config: A dictionary object with the parameters.
        :param kwargs: Dynamic list of params which supersedes config params if
                       they overlap.
        :param database: default database to use for operations
        :param server: server name
        :param table: name of the SQL Server table
        :param username: username for SQL login (default: None)
        :param password: password for SQL login (default: None)
        """
        super().__init__(config)
        self.schema = 'dbo'
        self.server = None
        self.database = None
        self.table = None
        self.username = None
        self.password = None
        input_args = set()
        if config:
            for key, value in config.items():
                setattr(self, key, value)
                input_args.add(key)
        for key, value in kwargs.items():
            setattr(self, key, value)
            input_args.add(key)
        required_args = {'server', 'database', 'table'}
        if not required_args.issubset(input_args):
            raise ValueError(
                f'Missing arguments in kwargs and config. '
                f'Need {required_args}')

    @property
    def with_krb_auth(self):
        """Returns True if the object uses Kerberos for authentication.
        :return: Kerberos authentication eligibility
        :rtype: bool
        """
        if hasattr(self, 'username') and hasattr(self, 'password') and self.username and self.password:
            result = False
        else:
            result = True
        return result


class DataFrame(DataObject):
    """Wrapper for pandas.DataFrame objects
    """

    def __init__(self, df):
        """
        :param df: DataFrame object
        :type df: pandas.DataFrame
        """
        super().__init__(dict())
        self._df = df
        self._flat_file_object = None

    def to_sql(self, sql_table, index=False, use_existing_sql_table=False, batch_size=10000):
        """Sends the object to SQL Server.
        :param sql_table: destination SQL Server table
        :type sql_table: SqlTable
        :param index: Specifies whether to send the index of
        the DataFrame or not
        :type index: bool
        :param use_existing_sql_table: If to use an existing table in the SQL database. 
        If not, then creates a new one.
        :type use_existing_sql_table: bool
        :param batch_size: Batch size (chunk size) to send to SQL Server
        :type batch_size: int
        """
        delimiter = ','
        qualifier = '"'
        newline = '\n'
        csv_file_path = TemporaryFile.get_tmp_file()
        self._df.to_csv(index=index, sep=delimiter, quotechar=qualifier,
                        quoting=csv.QUOTE_ALL,
                        line_terminator=newline,
                        path_or_buf=csv_file_path)
        self._flat_file_object = FlatFile(delimiter=',',
                                          qualifier=qualifier,
                                          newline=newline,
                                          path=csv_file_path)
        try:
            self._flat_file_object.to_sql(sql_table, use_existing_sql_table=use_existing_sql_table, batch_size=batch_size)
        finally:
            os.remove(csv_file_path)
