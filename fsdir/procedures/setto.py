from fsdir.core import Procedure
import fsdir.directives


class SetTo(Procedure):
    def is_applicable_to_directive(self, directive):
        return directive.__class__ == fsdir.directives.Edit

    def validate(self, dummy_fs, extract):
        """
        Should always receive two tokens, the first one always has to be non-blank, while the
        second one could be anything. List for multi-line and string for single line.

        :param dummy_fs:
        :param extract:
        :return:
        """
        if len(extract.tokens) != 2:
            return False

        if extract.tokens[0] == '':
            return False

        return True

    def run(self, dummy_fs, directive, extract):
        pass
