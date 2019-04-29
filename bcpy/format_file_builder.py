from .dict2xml import dict2xml


class FormatFile(object):
    @classmethod
    def _get_field_terminators(cls, flat_file):
        terminators = list()
        qualifier = cls._scaper(flat_file.qualifier)
        delimiter = cls._scaper(flat_file.delimiter)
        newline = cls._scaper(flat_file.newline)
        if flat_file.qualifier:
            terminators.append(qualifier)
        qualifier_delimiter_combo = str.format('{0}{1}{0}', qualifier, delimiter)
        terminators.extend([qualifier_delimiter_combo for i in range(len(flat_file.columns) - 1)])
        terminators.append(qualifier + newline)
        return terminators

    @staticmethod
    def _scaper(input_string):
        scaped_string = input_string.replace('"', '\\"').replace("'", "\\'").replace('\r', '\\r').replace('\n', '\\n')
        return scaped_string

    @classmethod
    def build_format_file(cls, flat_file):
        format_file_row_count = len(flat_file.columns)+1 if flat_file.qualifier else len(flat_file.columns)
        format_file = f'9.0\n{format_file_row_count}\n'
        terminators = cls._get_field_terminators(flat_file)
        if flat_file.qualifier:
            format_file += f'1 SQLCHAR 0 0 "{terminators[0]}" 0 ignored_line_start_qualifier SQL_Latin1_General_CP1_CI_AS\n'
            format_file_row_index = 2
            terminators = terminators[1:]
        else:
            format_file_row_index = 1
        for column_index, terminator in enumerate(terminators, 1):
            format_file += f'{format_file_row_index} SQLCHAR 0 0 "{terminator}" {column_index} {flat_file.columns[column_index - 1]} SQL_Latin1_General_CP1_CI_AS\n'
            format_file_row_index += 1
        return format_file
