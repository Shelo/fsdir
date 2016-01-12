from fsdir.core import Directive
import os


class Remove(Directive):
    def validate(self, dummy_fs, extract):
        """
        Validates that all files passed already exist. There should not be blank strings.

        :param extract:
        :param temp_files:
        :return:
        """
        if len(extract.tokens) == 0:
            return False

        for file_path in extract.tokens:
            if file_path == '':
                return False

            if not dummy_fs.isfile(file_path):
                return False

        return True

    def run(self, extract):
        pass
