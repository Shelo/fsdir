from fsdir.core import Directive, DummyFileSystem
from fsdir.fsdirector import Extract


class Edit(Directive):
    def __init__(self):
        super(Edit, self).__init__()

        self.file = []

    def validate(self, dummy_fs, extract, procedure):
        """


        :type dummy_fs: DummyFileSystem
        :type extract: Extract

        :param dummy_fs:
        :param extract:

        :return:
        """
        for file_path in extract.tokens:
            # should validate that the file actually exists.
            if not file_path or not dummy_fs.isfile(file_path):
                extract.error = "File does not exists."
                return False

        if not procedure:
            extract.error = "Should always be called with a procedure."
            return False

        return True

    def run(self, dummy_fs, extract, procedure):
        """
        :type dummy_fs: DummyFileSystem
        :type extract: Extract
        """
        # read the file's content.
        with dummy_fs.open_file(extract.tokens[0]) as source:
            for line in source:
                self.file.append(line)

        # call the procedure with the file.
        self.call_procedure(procedure, dummy_fs, extract)

        # save the new file.
        with dummy_fs.open_file(extract.tokens[0], "w+") as source:
            for line in self.file:
                source.write(line)
