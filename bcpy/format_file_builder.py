class FormatFile:
    @classmethod
    def _get_field_terminators(cls, flat_file):
        """Returns the field terminators that a bcp format file requires
        :param flat_file: Source flat file
        :type flat_file: FlatFile
        """
        terminators = list()
        qualifier = cls._scaper(flat_file.qualifier)
        delimiter = cls._scaper(flat_file.delimiter)
        newline = cls._scaper(flat_file.newline)
        if flat_file.qualifier:
            terminators.append(qualifier)
        qualifier_delimiter_combo = str.format(
            '{0}{1}{0}',
            qualifier,
            delimiter)
        terminators.extend(
            [qualifier_delimiter_combo
             for _ in range(len(flat_file.columns) - 1)])
        terminators.append(qualifier + newline)
        return terminators

    @staticmethod
    def _scaper(input_string):
        """Adds the required scape characters to the format file.
        :param input_string: Value before scaping
        :type input_string: str
        :return: Scaped string
        """
        scaped_string = input_string.replace('"', '\\"').replace("'", "\\'") \
            .replace('\r', '\\r').replace('\n', '\\n')
        return scaped_string

    @classmethod
    def build_format_file(cls, data_object):
        """Builds the format file for a given file with columns attribute
        :param data_object: An object that has a list attribute with the name
                            of 'columns'
        :return: String value of the format file
        :rtype: str
        """
        if data_object.qualifier:
            format_file_row_count = len(data_object.columns) + 1
        else:
            format_file_row_count = len(data_object.columns)
        format_file = f'9.0\n{format_file_row_count}\n'
        terminators = cls._get_field_terminators(data_object)
        if data_object.qualifier:
            format_file += f'1 SQLCHAR 0 0 "{terminators[0]}" 0 ' \
                f'ignored_line_start_qualifier SQL_Latin1_General_CP1_CI_AS\n'
            format_file_row_index = 2
            terminators = terminators[1:]
        else:
            format_file_row_index = 1
        for column_index, terminator in enumerate(terminators, 1):
            format_file += f'{format_file_row_index} SQLCHAR 0 0 ' \
                f'"{terminator}" {column_index} ' \
                f'{data_object.columns[column_index - 1]} ' \
                f'SQL_Latin1_General_CP1_CI_AS\n'
            format_file_row_index += 1
        return format_file
