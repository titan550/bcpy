from .dict2xml import dict2xml


class FormatFile(object):

    @staticmethod
    def _get_fields_format(columns):
        output = list()
        for i, column in enumerate(columns, 1):
            field = {
                'ID': i
                ,'xsi:type': 'CharTerm'
                ,'TERMINATOR': ','
                ,'MAX_LENGTH': 'MAX'
                ,'COLLATION': 'SQL_Latin1_General_CP1_CI_AS'
            }
            output.append(field)
        return output

    @staticmethod
    def _get_row_format(columns):
        output = list()
        for i, column in enumerate(columns, 1):
            row = {
                'SOURCE': i,
                'NAME': column,
                'xsi:type': 'SQLNVARCHAR'
            }
            output.append(row)
        return output

    @staticmethod
    def build_format_file(input_file):
        format = {
            'xmlns': 'https://schemas.microsoft.com/sqlserver/2004/bulkload/format',
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'RECORD': {
                'FIELD': FormatFile._get_fields_format(input_file.columns.to_list())
            },
            'ROW':{
                'COLUMN': FormatFile._get_row_format(input_file.columns.to_list())
            }
        }
        xml_output = dict2xml(format, 'BCPFORMAT')
        return xml_output
