from fsdir.core import Directive


class Create(Directive):
    def validate(self, dummy_fs, extract):
        for file_path in extract.tokens:
            if not file_path:
                return False
            else:
                if dummy_fs.isfile(file_path):
                    # error, the file already exists.
                    return False
                else:
                    dummy_fs.append(file_path)

        return True

    def run(self, dummy_fs, extract):
        for file_path in extract.tokens:
            dummy_fs.create_file(file_path)
