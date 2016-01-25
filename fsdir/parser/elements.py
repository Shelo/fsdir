import inspect

from fsdir.parser.indexdata import IndexData
from fsdir.parser.tokenizer import Tokenizer


class ElementParser(object):
    TYPE_DIRECTIVE = 1
    TYPE_DIRECTIVE_PARAMS = 2
    TYPE_PROCEDURE = 3
    TYPE_PROCEDURE_PARAMS = 4
    TYPE_END_COMMAND = 5
    TYPE_IGNORE = -1

    def __init__(self, tokens):
        self.tokens = tokens

        self.elements = []
        self.cursor = 0

        # state.
        self.in_command = False

        self.process()

    def process(self):
        while self.cursor < len(self.tokens):
            self.process_token(self.tokens[self.cursor])

    def process_token(self, token):
        data = IndexData()

        if token.type == Tokenizer.TYPE_IDENTIFIER:
            self.parse_identifier(data)
        elif token.type == Tokenizer.TYPE_FILE_PATH:
            self.parse_directive_params(data)
            self.parse_directive_params(data)
        elif token.type == Tokenizer.TYPE_PARAMETER:
            self.parse_procedure_params(data)
        elif token.type == Tokenizer.TYPE_TEXT_PARAMETER:
            self.parse_procedure_params(data)
        elif token.type == Tokenizer.TYPE_NEWLINE:
            self.parse_newline(data)
        elif token.type == Tokenizer.TYPE_COMMENT:
            self.parse_comment(data)
        else:
            raise ValueError("Semantic error.")

        data.position = self.cursor
        if data.type != self.TYPE_IGNORE:
            self.elements.append(data)

        self.cursor += data.length

    # - Util
    @staticmethod
    def get_types():
        types = {}

        for name, value in inspect.getmembers(ElementParser,
                lambda a: type(a) == int):
            if name.startswith("TYPE"):
                formatted = name.replace("TYPE_", "")
                formatted = formatted.replace("_", " ")
                formatted = formatted.title()

                types[value] = formatted

        return types

    # - Parsers
    def parse_identifier(self, data):
        if not self.in_command:
            self.in_command = True
            self.parse_directive(data)
        else:
            self.parse_procedure(data)

    def parse_directive(self, data):
        data.type = self.TYPE_DIRECTIVE

        # expects at least one file path.
        t_cursor = self.cursor + 1

        if t_cursor >= len(self.tokens) or \
                self.tokens[t_cursor].type != Tokenizer.TYPE_FILE_PATH:
            raise ValueError("Directive needs at least one argument.")

        data.length = 1

    def parse_directive_params(self, data):
        data.type = self.TYPE_DIRECTIVE_PARAMS

        t_cursor = self.cursor + 1

        while t_cursor < len(self.tokens) and \
                self.tokens[t_cursor].type == Tokenizer.TYPE_FILE_PATH:
            t_cursor += 1

        data.length = t_cursor - self.cursor

    def parse_procedure(self, data):
        data.type = self.TYPE_PROCEDURE
        data.length = 1

    def parse_procedure_params(self, data):
        data.type = self.TYPE_PROCEDURE_PARAMS

        t_cursor = self.cursor + 1

        while t_cursor < len(self.tokens) and \
                self.tokens[t_cursor].type == Tokenizer.TYPE_PARAMETER or \
                self.tokens[t_cursor].type == Tokenizer.TYPE_TEXT_PARAMETER:
            t_cursor += 1

        data.length = t_cursor - self.cursor

    def parse_newline(self, data):
        self.in_command = False
        data.type = self.TYPE_END_COMMAND
        data.length = 1

    def parse_comment(self, data):
        data.type = self.TYPE_IGNORE
        data.length = 1
