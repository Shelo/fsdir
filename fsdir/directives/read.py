from fsdir.core import Directive
import os


class Read(Directive):
    """
    Reads one file, storing the content as an internal list of string lines, ignores
    every change to that list.
    """

    def __init__(self):
        super(Read, self).__init__()

        self.lines = []

    def validate(self, dummy_fs, extract, procedure):
        """
        Validate that there's only one file, and that file actually exists.
        """
        if len(extract.tokens) != 1:
            return False

        if dummy_fs.isfile(extract.tokens[0]):
            return True

        return False

    def begin(self, dummy_fs, extract):
        """
        Read each line in the file and store its lines.
        """
        with dummy_fs.open_file(extract.tokens[0]) as source:
            for line in source:
                self.lines.append(line)

    def end(self, dummy_fs, extract):
        pass
