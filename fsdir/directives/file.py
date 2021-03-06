from fsdir.core import IterativeDirective


class File(IterativeDirective):
    """
    Base directive that simply selects a file (or files) to pass it to a
    procedure.
    """

    def __init__(self):
        super(File, self).__init__()

    def validate(self, dummy_fs, extract, procedure):
        for file_path in extract.tokens:
            if not dummy_fs.isfile(file_path):
                extract.error = "File %s does not exists." % file_path
                return False

        return True

    def begin(self, dummy_fs, extract):
        for file_path in extract.tokens:
            self.append(file_path)

    def end(self, dummy_fs, extract):
        pass
