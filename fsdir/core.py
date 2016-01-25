import collections
import os
import shutil


class DummyFileSystem(object):
    """
    The dummy file system is a file system resource manager that has the
    ability to fake transactions, using sandbox, so that the directives and
    procedures can work without knowing that, and so, don't repeat code, allow
    for safety, less errors, etc.

    Basically, this is a layer of abstraction.
    """

    def __init__(self):
        self.temp_files = []
        self._prefix = ""
        self._sandbox = False

    def begin_sandbox(self, sb_dir):
        """
        Start the dummy file system using a sandbox directory.

        :param sb_dir:
        """
        self._prefix = sb_dir
        self._sandbox = True

    def end_sandbox(self):
        """
        Stops the sandbox behavior.

        :return:
        """
        self._prefix = ""
        self._sandbox = False

    def is_sandbox(self):
        return self._sandbox

    def register_file(self, file_path):
        self.temp_files.append(file_path)

    def isfile(self, file_path):
        return os.path.isfile(file_path) or file_path in self.temp_files

    def exists(self, file_path):
        return os.path.exists(file_path) or file_path in self.temp_files

    def get_canonical_path(self, file_path):
        """
        The canonical path is a path that considers the current state of this
        file system.

        :param file_path:       the path to be converted.
        :return:                the canonical path.
        """
        return os.path.join(self._prefix, file_path)

    def open_file(self, file_path, mode="r"):
        canonical_path = self.get_canonical_path(file_path)

        basedir = os.path.dirname(canonical_path)
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        # check that the file was not previously copied.
        if not os.path.isfile(canonical_path):
            shutil.copy(file_path, canonical_path)

        return open(canonical_path, mode)

    def create_file(self, file_path):
        # add a second security.
        if os.path.isfile(file_path):
            raise ValueError("Creation failed: %s already exists." % file_path)

        self.open_file(file_path, mode="w").close()

    def chmod(self, file_path, mode):
        self.open_file(file_path).close()
        os.chmod(self.get_canonical_path(file_path), mode)


class Instruction(object):
    def __init__(self):
        self.name = self.__class__.__name__.upper()

    def keyword(self):
        return self.name


class Directive(Instruction):
    """
    Directives are instructions that can work with files.
    """
    def validate(self, dummy_fs, extract, procedure):
        raise NotImplementedError

    def begin(self, dummy_fs, extract):
        raise NotImplementedError

    def end(self, dummy_fs, extract):
        raise NotImplementedError

    def next(self):
        raise NotImplementedError

    def repeat_each_file(self):
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


class IterativeDirective(Directive):
    def __init__(self):
        super(IterativeDirective, self).__init__()

        self.__iterable = []
        self.index = -1
        self.item = None

    def append(self, item):
        self.__iterable.append(item)

    def repeat_each_file(self):
        return True

    def next(self):
        self.index += 1
        self.item = self.__iterable[self.index]
        return self.item

    def restart(self):
        self.item = None
        self.index = -1

    def get_current(self):
        return self.item

    def get_index(self):
        return self.index

    def set(self, index, value):
        self.__iterable[index] = value

    def end(self, dummy_fs, extract):
        raise NotImplementedError

    def validate(self, dummy_fs, extract, procedure):
        raise NotImplementedError

    def begin(self, dummy_fs, extract):
        raise NotImplementedError
