from fsdir.parser.tokenizer import Tokenizer
from fsdir.parser.elements import ElementParser


class Command(object):
    """
    Single command that contains a directive, a procedure and parameters for
    each one. The procedure can be None if there's no need for one.
    """

    def __init__(self):
        self.directive = None
        self.procedure = None

        self.directive_params = []
        self.procedure_params = []

    def add_directive_params(self, value):
        self.directive_params.append(value)

    def add_procedure_params(self, value):
        self.procedure_params.append(value)

    def __str__(self):
        return "%s\n\t%s\n\t%s\n\t%s" % (
            self.directive,
            ";".join(self.directive_params),
            self.procedure,
            repr(";".join(self.procedure_params))
        )


class FSDirParser(object):
    def __init__(self):
        self.tokens = None
        self.source = None
        self.elements = None

        self.command = None
        self.commands = []

    def parse_s(self, source):
        self.source = source

        # get parsed tokens.
        tokenizer = Tokenizer(source)
        self.tokens = tokenizer.tokens

        # get parsed elements.
        element_parser = ElementParser(self.tokens)
        self.elements = element_parser.elements

        # index each element into commands.
        self.index_elements()

        return self.commands

    def index_elements(self):
        # create the current command.
        self.command = Command()

        # for each element in the elements try to fill the command with
        # instructions.
        for element in self.elements:
            if element.type == ElementParser.TYPE_DIRECTIVE:
                self.command.directive = self.identifier_substring(element)
            elif element.type == ElementParser.TYPE_DIRECTIVE_PARAMS:
                self.command.directive_params = self.identifier_params(element)
            elif element.type == ElementParser.TYPE_PROCEDURE:
                self.command.procedure = self.identifier_substring(element)
            elif element.type == ElementParser.TYPE_PROCEDURE_PARAMS:
                self.command.procedure_params = self.identifier_params(element)
            elif element.type == ElementParser.TYPE_END_COMMAND:
                # when the command is over, push the command to the list,
                self.commands.append(self.command)
                # and create a new one to start again.
                self.command = Command()

    def identifier_substring(self, data):
        token = self.tokens[data.position]

        # get the string for a single token.
        return self.source[token.position:token.position + token.length]

    def identifier_params(self, data):
        params = []

        tokens = self.tokens[data.position:data.position + data.length]

        # fill the params list with substring for each token in the range.
        for token in tokens:
            params.append(self.source[token.position:token.position +
                    token.length])

        return params

    def debug(self):
        types = Tokenizer.get_types()

        print "TOKEN TYPE".ljust(16), "LENGTH".rjust(6), "  ", "CONTAINS"
        for token in self.tokens:
            t_type = types[token.type].ljust(16)
            t_length = str(token.length).rjust(6)
            t_stop = token.position + token.length
            t_repr = repr(self.source[token.position:t_stop])
            print t_type, t_length, "  ", t_repr

        types = ElementParser.get_types()

        print
        print "ELEMENT TYPE".ljust(16), "LENGTH".rjust(6)
        for element in self.elements:
            print types[element.type].ljust(16), str(element.length).rjust(6)

        print
        for instruction in instructions:
            print instruction


if __name__ == '__main__':
    parser = FSDirParser()

    instructions = None
    with open("example/dev.fsdir") as f:
        instructions = parser.parse_s(f.read())
    parser.debug()
