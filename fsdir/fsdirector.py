import re
import os
import shutil
import util.treedisplay
from fsdir.core import DummyFileSystem
from fsdir.parser import FSDirParser
from fsdir.util import argscontrol


class Extract(object):
    def __init__(self, kw, tokens, sub_extract=None):
        self.keyword = kw
        self.tokens = tokens
        self.sub_extract = sub_extract
        self.error = None


class FSDirector(object):
    """
    File System Director.

    <need for a better explanation here>
    """

    sandbox_dir = ".sandbox"

    def __init__(self):
        self.cache = []

        self.directives = []
        self.procedures = []

        self.dummy_fs = DummyFileSystem()

        self.display = False

    def load(self, file_path):
        """
        Run director from file.

        :param file_path:    the path of the .fsdir script.
        :return:
        """
        with open(file_path) as script_file:
            script = script_file.read()

        self.loads(script)

    def loads(self, script):
        """
        Run director with a given string.

        :param script:      script as string.
        :return:
        """
        parser = FSDirParser()
        commands = parser.parse_s(script)

        for command in commands:
            self.index_command(command)

    def index_command(self, command):
        directive = self.find_directive(command.directive)
        files = command.directive_params

        directive_copy = directive.__class__()
        procedure_copy = None

        sub_extract = None

        if command.procedure:
            args = command.procedure_params
            procedure = self.find_procedure(command.procedure)
            procedure_copy = procedure.__class__()

            sub_extract = Extract(procedure.keyword(), args)

        extract = Extract(directive.keyword(), files, sub_extract)

        self.cache.append((directive_copy, procedure_copy, extract))

    def validate(self):
        """
        Validates every step to be taken.

        :return:
        """
        for directive, procedure, extract in self.cache:
            if not directive.validate(self.dummy_fs, extract, procedure):
                raise ValueError(
                    "[%d] Directive %s cannot take the values: %s (%s)" %
                    (extract.line, directive.keyword(), str(extract.tokens),
                    extract.error)
                )

            if procedure:
                self.validate_procedure(procedure, directive,
                        extract.sub_extract)

        return True

    def validate_procedure(self, procedure, directive, extract):
        if not procedure.is_applicable_to_directive(directive):
            raise ValueError(
                "Procedure %s is not applicable to the directive: %s" %
                (procedure.keyword(), directive.keyword())
            )

        if not procedure.validate(self.dummy_fs, extract):
            raise ValueError(
                "Procedure %s cannot take the values: %s" %
                (procedure.keyword(), str(extract.tokens))
            )

    def run(self):
        pass

    def sandbox_run(self):
        """
        Run the director as a sandbox test.
        """
        self.begin_sandbox_dir()

        self.dummy_fs.begin_sandbox(self.sandbox_dir)

        for directive, procedure, extract in self.cache:
            directive.begin(self.dummy_fs, extract)

            if procedure:
                self._run_procedure(directive, procedure, extract)

            directive.end(self.dummy_fs, extract)

        # TODO: just for development stages.
        # self.stop_sandbox_dir()

        self.post_process()

    def _run_procedure(self, directive, procedure, extract):
        if directive.repeat_each_file():
            for _ in extract.tokens:
                directive.next()
                procedure.run(self.dummy_fs, directive, extract.sub_extract)
        else:
            procedure.run(self.dummy_fs, directive, extract.sub_extract)

    def find_directive(self, keyword):
        """
        Finds the directive that matches the name of the extract given.

        Raises a ValueError exception if nothing is found.

        :param keyword:     the keyword to match.
        :return:            the directive.
        """
        for directive in self.directives:
            if directive.keyword() == keyword:
                return directive

        raise ValueError(
            "Not a valid directive: %s" % keyword
        )

    def find_procedure(self, keyword):
        """
        Finds the procedure that matches the name of the extract given.

        Raises a ValueError exception if nothing is found.

        :param keyword:     the keyword to match.
        :return:            the procedure.
        """
        for procedure in self.procedures:
            if procedure.keyword() == keyword:
                return procedure

        raise ValueError(
            "Not a valid procedure: %s" % keyword
        )

    def load_procedure(self, procedure):
        """
        Load a particular procedure plugin.

        :param procedure:       the procedure to load.
        :return:
        """
        self.procedures.append(procedure())

    def load_directive(self, directive):
        """
        Load a particular directive plugin.

        :param directive:       the directive to load.
        :return:
        """
        self.directives.append(directive())

    def begin_sandbox_dir(self):
        """
        Prepares the sandbox directory.
        """
        if os.path.exists(self.sandbox_dir):
            shutil.rmtree(self.sandbox_dir)

        os.mkdir(self.sandbox_dir)

    def end_sandbox_dir(self):
        if os.path.exists(self.sandbox_dir):
            shutil.rmtree(self.sandbox_dir)

    def apply(self, keep=False):
        if not os.path.exists(self.sandbox_dir):
            raise AssertionError(
                "Sandbox directory does not exists, call sandbox_run() first."
            )

        if not keep:
            self.end_sandbox_dir()

    def load_argv(self):
        argscontrol.config_argv(self)

    def post_process(self):
        if self.display:
            self.display_sandbox()

    def display_sandbox(self):
        util.treedisplay.display(self.sandbox_dir)
