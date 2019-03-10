import os
import pandas as pd
import random, string
import tempfile
from .format_file_builder import FormatFile

name = "bcpy"


def _to_csv(input):
    csv_file_name = os.path.join(_get_tmp_dir(), ''.join(random.choices(string.ascii_letters + string.digits, k=21)))
    if type(input) == pd.DataFrame:
        input.to_csv(csv_file_name)
    else:
        raise NotImplementedError
    return csv_file_name


def _get_tmp_dir():
    if os.name == 'posix':
        tmp_file_path = '/dev/shm'
    else:
        tmp_file_path = tempfile.gettempdir()
    return tmp_file_path


def _bcp(csv_file_path, formaet_file_path, sql_info):
    # TODO call shell comamnd bcp
    pass


def _build_format_file(input):
    xml_format_file_content = FormatFile.build_format_file(input)
    format_file_path = os.path.join(_get_tmp_dir(), ''.join(random.choices(string.ascii_letters + string.digits, k=21)))
    with open(format_file_path, 'w') as f:
        f.write(xml_format_file_content)
    return format_file_path


def to_sql(input, sql_info):
    csv_file_path = _to_csv(input)
    format_file_path = _build_format_file(input)
    _bcp(csv_file_path, format_file_path, sql_info)
    os.remove(csv_file_path)
    os.remove(format_file_path)
