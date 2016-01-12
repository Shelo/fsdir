import os


class DummyFileSystem(object):
    def __init__(self):
        self.temp_files = []

    def append(self, file_path):
        self.temp_files.append(file_path)

    def isfile(self, file_path):
        return os.path.isfile(file_path) or file_path in self.temp_files

    def exists(self, file_path):
        return os.path.exists(file_path) or file_path in self.temp_files


class Instruction(object):
    def __init__(self):
        self.name = self.__class__.__name__.upper()

    def keyword(self):
        return self.name

    def run(self, extract):
        raise NotImplementedError


class Directive(Instruction):
    """
    Directives are instructions that can work with files.
    """
    def validate(self, dummy_fs, extract):
        raise NotImplementedError


class Procedure(Instruction):
    """
    Procedures are instructions that complements directives.
    """
    def validate(self, dummy_fs, extract):
        raise NotImplementedError

    def is_applicable_to_directive(self, directive):
        raise NotImplementedError
