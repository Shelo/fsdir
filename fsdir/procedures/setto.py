from fsdir.core import Procedure
import fsdir.directives
import re


class SetTo(Procedure):
    def is_applicable_to_directive(self, directive):
        return directive.__class__ == fsdir.directives.Edit

    def validate(self, dummy_fs, extract):
        """
        Should always receive two tokens, the first one always has to be non-blank, while the
        second one could be anything. List for multi-line and string for single line.
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
        matcher = re.compile(extract.tokens[0])

        replacement = "\n".join(extract.tokens[1]) if type(extract.tokens[1] == list) \
            else extract.tokens[1]

        for index, line in enumerate(directive.file):
            if matcher.match(line):
                directive.file[index] = replacement
