import os


class DummyFileSystem(object):
    def __init__(self):
        self.temp_files = []
        self._prefix = ""
        self._sandbox = False

    def set_prefix(self, prefix):
        self._prefix = prefix
        self._sandbox = True if prefix else False

    def is_sandbox(self):
        return self._sandbox

    def append(self, file_path):
        self.temp_files.append(file_path)

    def isfile(self, file_path):
        return os.path.isfile(file_path) or file_path in self.temp_files

    def exists(self, file_path):
        return os.path.exists(file_path) or file_path in self.temp_files

    def get_canonical_path(self, file_path):
        return os.path.join(self._prefix, file_path)

    def open_file(self, file_path):
        path = self.get_canonical_path(file_path)

        basedir = os.path.dirname(path)
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        return open(path, "w+")

    def create_file(self, file_path):
        self.open_file(file_path).close()


class Instruction(object):
    def __init__(self):
        self.name = self.__class__.__name__.upper()

    def keyword(self):
        return self.name


class Directive(Instruction):
    """
    Directives are instructions that can work with files.
    """
    def validate(self, dummy_fs, extract):
        raise NotImplementedError

    def run(self, dummy_fs, extract):
        raise NotImplementedError


class Procedure(Instruction):
    """
    Procedures are instructions that complements directives.
    """
    def validate(self, dummy_fs, extract):
        raise NotImplementedError

    def is_applicable_to_directive(self, directive):
        raise NotImplementedError

    def run(self, dummy_fs, directive, extract):
        raise NotImplementedError
