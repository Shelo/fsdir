from fsdir.core import Directive


class Remove(Directive):
    def validate(self, dummy_fs, extract, procedure):
        """
        Validates that all files passed already exist. There should not be
        blank strings.

        :param dummy_fs:
        :param extract:
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

    def begin(self, dummy_fs, extract):
        pass

    def end(self, dummy_fs, extract):
        pass
