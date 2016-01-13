from fsdir.core import Directive


class Create(Directive):
    def validate(self, dummy_fs, extract, procedure):
        for file_path in extract.tokens:
            if not file_path:
                return False
            else:
                if dummy_fs.isfile(file_path):
                    # error, the file already exists.
                    return False
                else:
                    dummy_fs.register_file(file_path)

        return True

    def begin(self, dummy_fs, extract):
        for file_path in extract.tokens:
            dummy_fs.create_file(file_path)

    def end(self, dummy_fs, extract):
        pass
