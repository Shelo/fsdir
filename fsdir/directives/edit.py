from fsdir.core import Directive, DummyFileSystem
from fsdir.fsdirector import Extract


class Edit(Directive):
    def __init__(self):
        super(Edit, self).__init__()

        self.files = []

    def validate(self, dummy_fs, extract, procedure):
        """
        Always validate that the file already exists or has been created
        previously, also, this always has to be called with a procedure, by it self, this
        does nothing meaningful.
        """
        for file_path in extract.tokens:
            # should validate that the file actually exists.
            if not file_path or not dummy_fs.isfile(file_path):
                extract.error = "File %s does not exists." % file_path
                return False

        if not procedure:
            extract.error = "Should always be called with a procedure."
            return False

        return True

    def begin(self, dummy_fs, extract):
        """
        :type dummy_fs: DummyFileSystem
        :type extract: Extract
        """
        # read the file's content.
        for file_path in extract.tokens:
            lines = []

            with dummy_fs.open_file(file_path) as source:
                for line in source:
                    lines.append(line)

            self.files.append(lines)

    def end(self, dummy_fs, extract):
        """
        :type dummy_fs: DummyFileSystem
        :type extract: Extract
        """
        # save the new file.
        for i, file_path in enumerate(extract.tokens):
            lines = self.files[i]

            with dummy_fs.open_file(file_path, "w+") as source:
                for line in lines:
                    source.write(line)
