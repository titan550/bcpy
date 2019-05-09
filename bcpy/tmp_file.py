import os
import random
import string
import sys
import tempfile


class TemporaryFile:
    tmp_dir = None

    def __init__(self, mode='w'):
        self._file_path = self.get_tmp_file()
        self._tmp_file = open(self._file_path, mode)

    def __enter__(self):
        return self._tmp_file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._tmp_file.close()

    @classmethod
    def _get_tmp_dir(cls):
        """
        :return: The optimum temporary directory based on OS and environment
        :rtype: str
        """
        if cls.tmp_dir:
            tmp_dir = cls.tmp_dir
        elif sys.platform == 'linux':
            try:
                tmp_dir = os.environ['XDG_RUNTIME_DIR']
            except KeyError:
                tmp_dir = None
            if not tmp_dir:
                tmp_dir = '/dev/shm'
        else:
            tmp_dir = tempfile.gettempdir()
        return tmp_dir

    @classmethod
    def get_tmp_file(cls):
        """Returns full path to a temporary file without creating it.
        :return: Full path to a temporary file
        :rtype: str
        """
        tmp_dir = cls._get_tmp_dir()
        file_path = os.path.join(tmp_dir, ''.join(
            random.choices(string.ascii_letters + string.digits, k=21)))
        return file_path
