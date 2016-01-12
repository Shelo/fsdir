from fsdir.core import Directive
import os


class Edit(Directive):
    def validate(self, dummy_fs, extract):
        for file_path in extract.tokens:
            # should validate that the file actually exists.
            if not file_path or not dummy_fs.isfile(file_path):
                return False

        return True

    def run(self, extract):
        pass
