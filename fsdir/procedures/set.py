from fsdir.core import Procedure
import fsdir.directives
import re


class Set(Procedure):
    def is_applicable_to_directive(self, directive):
        return directive.__class__ == fsdir.directives.Edit

    def validate(self, dummy_fs, extract):
        """
        Should always receive one token.
        """
        if len(extract.tokens) != 1:
            return False

        return True

    def run(self, dummy_fs, directive, extract):
        """
        Search for all matches in the source file and replaces them.
        """
        replacement = extract.tokens[0]

        for i in range(len(directive.files)):
            if type(replacement) == list:
                directive.files[i] = '\n'.join(replacement)
            else:
                directive.files[i] = replacement
