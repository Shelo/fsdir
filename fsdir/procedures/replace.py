from fsdir.core import Procedure
import fsdir.directives
import re


class Replace(Procedure):
    def __init__(self):
        super(Replace, self).__init__()

        self.matcher = None

    def is_applicable_to_directive(self, directive):
        return directive.__class__ == fsdir.directives.Edit

    def validate(self, dummy_fs, extract):
        """
        Should always receive two tokens, the first one always has to be
        non-blank, while the second one could be anything. List for multi-line
        and string for single line.
        """
        if len(extract.tokens) != 2:
            return False

        if extract.tokens[0] == '':
            return False

        return True

    def run(self, dummy_fs, directive, extract):
        """
        Search for all matches in the source file and replaces them.
        """
        if not self.matcher:
            self.matcher = re.compile(extract.tokens[0])

        lines = directive.get_current()

        self.find_and_replace(lines, self.matcher, extract.tokens[1])

    @staticmethod
    def find_and_replace(lines, matcher, replacement):
        for index, line in enumerate(lines):
            if matcher.match(line):
                lines[index] = replacement

                if line[-1] == '\n':
                    lines[index] += '\n'
