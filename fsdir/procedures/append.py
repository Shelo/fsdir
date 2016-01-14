from fsdir.core import Procedure
import fsdir.directives


class Append(Procedure):
    def is_applicable_to_directive(self, directive):
        return directive.__class__ == fsdir.directives.Edit

    def validate(self, dummy_fs, extract):
        # there's nothing that we couldn't append.
        return True

    def run(self, dummy_fs, directive, extract):
        for lines in directive.files:
            for arg in extract.tokens:
                if type(arg) == list:
                    lines.append('\n'.join(arg) + "\n")
                else:
                    lines.append(arg + "\n")
