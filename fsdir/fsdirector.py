import re
from fsdir.core import DummyFileSystem


class Extract(object):
    def __init__(self, kw, tokens, line, sub_extract=None):
        self.keyword = kw
        self.tokens = tokens
        self.sub_extract = sub_extract
        self.line = line
        self.error = None


class FSDirector(object):
    """
    File System Director.

    This director fully validates a script before running, in order to maintain the file system safe
    for incomplete code.
    """

    directive_regex = re.compile("([A-Z]+) *((?:'[^']*' *)+) *(.*)")
    procedure_regex = re.compile("([A-Z]+) *( *\(.*\) *)* *(\{?)")

    def __init__(self):
        self.cache = []

        self.directives = []
        self.procedures = []

        self.lines = []
        self.current_line = 0

        self.dummy_fs = DummyFileSystem()

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
        self.lines = [line for line in script.split("\n")]

        while self.current_line < len(self.lines):
            line = self.lines[self.current_line]
            self.current_line += 1

            if line:
                self.process_line(line)

    def validate(self):
        """
        Validates every step to be taken.

        :return:
        """
        for directive, procedure, extract in self.cache:
            if not directive.validate(self.dummy_fs, extract):
                raise ValueError("[%d] Directive %s cannot take the values: %s" %
                                 (extract.line, directive.keyword(), str(extract.tokens)))

            if procedure:
                if not procedure.is_applicable_to_directive(directive):
                    raise ValueError("[%d] Procedure %s is not applicable to the directive: %s" %
                                     (extract.line, procedure.keyword(), directive.keyword()))

                if not procedure.validate(self.dummy_fs, extract.sub_extract):
                    raise ValueError("[%d] Procedure %s cannot take the values: %s" %
                                     (extract.line, procedure.keyword(),
                                      str(extract.sub_extract.tokens)))

        return True

    def run(self):
        pass

    def process_line(self, line):
        """
        Processes a single line of code. At the end, this should save a fully valid instruction
        to the instruction cache.

        :param line:        the line of code to process.
        :return:            a tuple with (directive, procedure, extract)
        """
        if line[0] == '#':
            return None

        extract = self.extract_directive(line)
        directive = self.match_directive(extract)

        procedure = None
        if extract.sub_extract:
            procedure = self.match_procedure(extract.sub_extract)

        self.cache.append((directive, procedure, extract))

    def extract_directive(self, source):
        """
        Matches a pattern and extracts the directive and procedure tokens from it.

        :param source:      the source code.
        :return:            the extracted call.
        """
        m = self.directive_regex.match(source)

        if m:
            sub_extract = None
            keyword = m.group(1)
            files = self.read_directive_args(m.group(2))

            if m.group(3):
                sub_extract = self.extract_procedure(m.group(3))

            return Extract(keyword, files, self.current_line, sub_extract=sub_extract)

        raise SyntaxError("[%d] Wrong line: %s" % (self.current_line, source))

    def extract_procedure(self, source):
        """
        Extracts data from a procedure.

        :param source:      the source code for the procedure.
        :return:            the extracted procedure.
        """
        m = self.procedure_regex.match(source)

        if m:
            keyword = m.group(1)
            args = self.read_procedure_args(m.group(2))

            if m.group(3):
                args.append(self.catch_lines())

            return Extract(keyword, args, self.current_line)

        return None

    def catch_lines(self):
        """
        Catches all lines until the multi-line ending "}".

        :return:    a list with all lines.
        """
        lines = []

        line = self.request_line()
        while line != "}":
            lines.append(line)
            line = self.request_line()

        return lines

    def request_line(self):
        """
        Request for one more line, skipping it through the regular pipeline.

        :return:    the next line of the source code.
        """
        self.current_line += 1
        return self.lines[self.current_line - 1]

    @staticmethod
    def read_procedure_args(source):
        """
        Reads simple arguments from a procedure.

        :param source:  the source code for the args.
        :return:        the arguments as a list.
        """
        args = []

        start = -1
        for index, char in enumerate(source):
            if start == -1:
                if char == '(':
                    start = index + 1
            else:
                if char == ')':
                    args.append(source[start:index])
                    start = -1

        return args

    @staticmethod
    def read_directive_args(source):
        """
        Reads simple arguments from a procedure.

        :param source:      the source code for the args.
        :return:            the arguments as a list.
        """
        args = []

        start = -1
        for index, char in enumerate(source):
            if start == -1:
                if char == '\'':
                    start = index + 1
            else:
                if char == '\'':
                    args.append(source[start:index])
                    start = -1

        return args

    def match_directive(self, extract):
        """
        Finds the directive that matches the name of the extract given.

        Raises a ValueError exception if nothing is found.

        :param extract:     the extract to match.
        :return:            the directive.
        """
        for directive in self.directives:
            if directive.keyword() == extract.keyword:
                return directive

        raise ValueError("[%d] Not a valid directive: %s" % (extract.line, extract.keyword))

    def match_procedure(self, extract):
        """
        Finds the procedure that matches the name of the extract given.

        Raises a ValueError exception if nothing is found.

        :param extract:     the extract to match.
        :return:            the procedure.
        """
        for procedure in self.procedures:
            if procedure.keyword() == extract.keyword:
                return procedure

        raise ValueError("[%d] Not a valid procedure: %s" % (extract.line, extract.keyword))

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
