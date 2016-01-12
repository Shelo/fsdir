from fsdir.core import Directive
import os


class Read(Directive):
    def validate(self, dummy_fs, extract):
        if len(extract.tokens) != 1:
            return False

        file_path = extract.tokens[0]

        if dummy_fs.isfile(file_path):
            return True

        return False

    def run(self, extract):
        pass
