from fsdir.core import Procedure
import fsdir.directives


class ChMod(Procedure):
    def is_applicable_to_directive(self, directive):
        return directive.__class__ == fsdir.directives.File

    def validate(self, dummy_fs, extract):
        """
        Should always receive the mod.
        """
        if len(extract.tokens) != 1:
            return False

        if not extract.tokens[0].isdigit():
            return False

        return True

    def run(self, dummy_fs, directive, extract):
        """
        Change very file in the directive to the needed mode.
        """
        for file_path in directive.files:
            dummy_fs.chmod(file_path, int(extract.tokens[0], 8))
