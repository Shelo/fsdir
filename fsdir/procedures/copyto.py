from fsdir.core import Procedure
import fsdir.directives


class CopyTo(Procedure):
    def is_applicable_to_directive(self, directive):
        return directive.__class__ == fsdir.directives.Read

    def validate(self, dummy_fs, extract):
        """
        Validate that all arguments passed are strings that can reference a real file.

        :param extract:     the extract of code.
        :return:            boolean indicating if it's valid or not.
        """
        for file_path in extract.tokens:
            if not file_path:
                return False

        return True

    def run(self, extract):
        pass
