import csv
import os

from .binary_callers import bcp, sqlcmd
from .format_file_builder import FormatFile
from .tmp_file import TemporaryFile


class DataObject:
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
        try:
        if self.__format_file_path:
            os.remove(self.__format_file_path)
        except AttributeError:
            pass

    def _read_columns_from_file(self):
        with open(self.path) as f:
            header = f.readline()
        qualifier_delimiter_combo = str.format('{0}{1}{0}', self.qualifier, self.delimiter)
        self.columns = [col for col in header.rstrip(self.newline).split(qualifier_delimiter_combo)]
        self.columns[0] = self.columns[0].lstrip(self.qualifier)
        self.file_has_header_line = True

    def get_format_file_path(self, recalculate=False):
        if not recalculate and self.__format_file_path:
            return self.__format_file_path
        else:
            try:
                if self.__format_file_path:
                    os.remove(self.__format_file_path)
            except OSError:
                pass
        if not self.columns:
            if self.path:
                self._read_columns_from_file()
            else:
                raise Exception('Need the object columns or path to build the format file')
        self.__format_file_path = self._build_format_file()
        return self.__format_file_path

    def _build_format_file(self):
        format_file_content = FormatFile.build_format_file(self)
        with TemporaryFile(mode='w') as f:
            f.write(format_file_content)
            format_file_path = f.name
        return format_file_path

    def to_sql(self, sql_table):
        bcp(sql_table, self)

    @property
    def columns(self):
        return self.__columns

    @columns.setter
    def columns(self, columns):
        if isinstance(columns, list):
            self.__columns = columns
        else:
            raise TypeError('Columns parameter must be a list of columns')


class SqlTable(DataObject):
    def __init__(self, config=dict(), **kwargs):
        super().__init__(config)
        self.schema = 'dbo'
        required_args = ['server', 'database', 'table']
        if not all(k in kwargs for k in required_args) and not all(k in config for k in required_args):
            raise ValueError(f'Missing arguments in kwargs and config. Need {required_args}')
        for key, value in config.items():
            setattr(self, key, value)
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def with_krb_auth(self):
        if hasattr(self, 'username') and hasattr(self, 'password'):
            result = False
        else:
            result = True
        return result


class DataFrame(DataObject):
    def __init__(self, df):
        super().__init__(dict())
        self._df = df
        self._csv_file_path = None
        self._flat_file_object = None

    def __del__(self):
        if self._csv_file_path:
            os.remove(self._csv_file_path)

    def to_sql(self, sql_table, index=False):
        delimiter = ','
        qualifier = '"'
        newline = '\n'
        self._csv_file_path = TemporaryFile.get_tmp_file()
        self._df.to_csv(index=index, sep=delimiter, quotechar=qualifier, quoting=csv.QUOTE_ALL,
                        line_terminator=newline, path_or_buf=self._csv_file_path)
        self._flat_file_object = FlatFile(delimiter=',', qualifier=qualifier, newline=newline, path=self._csv_file_path)
        self._flat_file_object.to_sql(sql_table)