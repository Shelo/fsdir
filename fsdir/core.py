class Instruction(object):
    def __init__(self):
        self.name = self.__class__.__name__.upper()

    def keyword(self):
        return self.name

    def validate(self, source):
        raise NotImplementedError

    def run(self, extract):
        raise NotImplementedError


class Procedure(Instruction):
    """
    Procedures are instructions that complements directives.
    """
    pass


class Directive(Instruction):
    """
    Directives are instructions that can work with files.
    """
    pass
