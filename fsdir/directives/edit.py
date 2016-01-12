from fsdir.core import Directive


class Edit(Directive):
    def keyword(self):
        return "EDIT"

    def validate(self, source):
        pass

    def run(self, extract):
        pass
