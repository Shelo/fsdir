import os
import inspect


class Index(object):
    def __init__(self, position=0, length=0, type=0):
        self.position = position
        self.length = length
        self.type = type


class IndexData(object):
    def __init__(self, length=0, type_=0, offset_start=0, offset_stop=0):
        self.length = length
        self.type = type_
        self.offset_start = offset_start
        self.offset_stop = offset_stop


class InstructionCall(object):
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


class Tokenizer(object):
    TYPE_IGNORE = 0
    TYPE_IDENTIFIER = 1
    TYPE_FILE_PATH = 2
    TYPE_PARAMETER = 3
    TYPE_BLANK_SPACE = 4
    TYPE_TEXT_PARAMETER = 5
    TYPE_COMMENT = 6
    TYPE_NEWLINE = 7

    CHAR_QUOTE = '\''
    CHAR_PARENTHESIS_LEFT = '('
    CHAR_PARENTHESIS_RIGHT = ')'
    CHAR_BRACE_LEFT = '{'
    CHAR_BRACE_RIGHT = '}'
    CHAR_COMMENT = '#'
    CHAR_SPACE = ' '
    CHAR_TAB = '\t'
    CHAR_NEWLINE = os.linesep

    def __init__(self, source):
        self.source = source
        self.cursor = 0
        self.tokens = []

        self.process()

    def process(self):
        while self.cursor < len(self.source):
            self.process_command(self.source[self.cursor])

    def process_command(self, c):
        data = IndexData()

        self.switch_parser(c, data)
        self.cursor += data.offset_start

        if data.type != self.TYPE_IGNORE:
            # do not include tokens that can be ignored.
            self.tokens.append(Index(self.cursor, data.length, data.type))

        self.cursor += data.length + data.offset_stop

    def switch_parser(self, c, data):
        if c.isupper():
            self.parse_identifier(data)
        elif self.is_space(c):
            self.parse_space(data)
        elif c == self.CHAR_QUOTE:
            self.parse_file_path(data)
        elif c == self.CHAR_PARENTHESIS_LEFT:
            self.parse_parameter(data)
        elif c == self.CHAR_BRACE_LEFT:
            self.parse_text_param(data)
        elif c == self.CHAR_COMMENT:
            self.parse_comment(data)
        elif c == self.CHAR_NEWLINE:
            self.parse_newline(data)
        else:
            raise ValueError("Wrong syntax: " + self.source[self.cursor:])

    # - Util
    def is_space(self, c):
        return c == self.CHAR_SPACE or c == self.CHAR_TAB

    @staticmethod
    def get_types():
        types = {}

        for name, value in inspect.getmembers(Tokenizer, lambda a: type(a) == int):
            if name.startswith("TYPE"):
                formatted = name.replace("TYPE_", "")
                formatted = formatted.replace("_", " ")
                formatted = formatted.title()

                types[value] = formatted

        return types

    # - Parsers
    def parse_identifier(self, data):
        """
        Parse language identifiers (commands).
        """
        # temporal cursor to move.
        t_cursor = self.cursor

        # check every letter until find a non-uppercase letter.
        while t_cursor < len(self.source) and self.source[t_cursor].isupper():
            t_cursor += 1

        data.length = t_cursor - self.cursor
        data.type = self.TYPE_IDENTIFIER

    def parse_space(self, data):
        """
        Parse non useful blank space.
        """
        t_cursor = self.cursor

        while t_cursor < len(self.source) and self.is_space(self.source[t_cursor]):
            t_cursor += 1

        data.type = self.TYPE_IGNORE
        data.length = t_cursor - self.cursor

    def parse_file_path(self, data):
        """
        Parse entire file path.
        """
        t_cursor = self.cursor + 1

        while t_cursor < len(self.source) and self.source[t_cursor] != self.CHAR_QUOTE:
            t_cursor += 1

        data.type = self.TYPE_FILE_PATH
        data.length = t_cursor - self.cursor - 1
        data.offset_start = 1
        data.offset_stop = 1

    def parse_parameter(self, data):
        """
        Parse a parameter (enclosed by parenthesis).
        """
        t_cursor = self.cursor + 1

        while t_cursor < len(self.source) and self.source[t_cursor] != self.CHAR_PARENTHESIS_RIGHT:
            t_cursor += 1

        data.type = self.TYPE_PARAMETER
        data.length = t_cursor - self.cursor - 1
        data.offset_start = 1
        data.offset_stop = 1

    def parse_text_param(self, data):
        """
        Parse a text parameter (enclosed by curly braces).
        """
        t_cursor = self.cursor + 1

        while t_cursor < len(self.source) and self.source[t_cursor] != self.CHAR_BRACE_RIGHT:
            t_cursor += 1

        data.type = self.TYPE_TEXT_PARAMETER
        data.length = t_cursor - self.cursor - 1
        data.offset_start = 1
        data.offset_stop = 1

        if self.source[t_cursor + 1] == self.CHAR_NEWLINE:
            data.offset_start += 1
            data.length -= 1

        if self.source[t_cursor - 1] == self.CHAR_NEWLINE:
            data.offset_stop += 1
            data.length -= 1

    def parse_comment(self, data):
        """
        Parse a comment (python-like comment).
        """
        t_cursor = self.cursor

        while t_cursor < len(self.source) and self.source[t_cursor] != self.CHAR_NEWLINE:
            t_cursor += 1

        data.type = self.TYPE_COMMENT
        data.length = t_cursor - self.cursor
        data.offset_stop = 1

    def parse_newline(self, data):
        """
        Parse the line break character.
        """
        t_cursor = self.cursor + 1

        while t_cursor < len(self.source) and self.source[t_cursor] == self.CHAR_NEWLINE:
            t_cursor += 1

        data.type = self.TYPE_NEWLINE
        data.length = t_cursor - self.cursor


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

        for name, value in inspect.getmembers(ElementParser, lambda a: type(a) == int):
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

        if t_cursor >= len(self.tokens) or self.tokens[t_cursor].type != Tokenizer.TYPE_FILE_PATH:
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


class Parser(object):
    def __init__(self):
        self.tokens = None
        self.source = None
        self.elements = None

        self.instructions = []

        self.instruction = None

    def parse_s(self, source):
        self.source = source

        tokenizer = Tokenizer(source)
        self.tokens = tokenizer.tokens

        element_parser = ElementParser(self.tokens)
        self.elements = element_parser.elements

        self.index_elements()

        return self.instructions

    def index_elements(self):
        self.instruction = InstructionCall()

        for element in self.elements:
            if element.type == ElementParser.TYPE_DIRECTIVE:
                self.instruction.directive = self.identifier_substring(element)
            elif element.type == ElementParser.TYPE_DIRECTIVE_PARAMS:
                self.instruction.directive_params = self.identifier_params(element)
            elif element.type == ElementParser.TYPE_PROCEDURE:
                self.instruction.procedure = self.identifier_substring(element)
            elif element.type == ElementParser.TYPE_PROCEDURE_PARAMS:
                self.instruction.procedure_params = self.identifier_params(element)
            elif element.type == ElementParser.TYPE_END_COMMAND:
                self.instructions.append(self.instruction)
                self.instruction = InstructionCall()

    def identifier_substring(self, data):
        token = self.tokens[data.position]
        return self.source[token.position:token.position + token.length]

    def identifier_params(self, data):
        params = []

        tokens = self.tokens[data.position:data.position + data.length]

        for token in tokens:
            params.append(self.source[token.position:token.position + token.length])

        return params

    def debug(self):
        types = Tokenizer.get_types()

        print "TOKEN TYPE".ljust(16), "LENGTH".rjust(6), "  ", "CONTAINS"
        for token in self.tokens:
            print types[token.type].ljust(16), str(token.length).rjust(6), "  ", \
                    repr(self.source[token.position:token.position + token.length])

        types = ElementParser.get_types()

        print
        print "ELEMENT TYPE".ljust(16), "LENGTH".rjust(6), "  "
        for element in self.elements:
            print types[element.type].ljust(16), str(element.length).rjust(6), "  "

        print
        for instruction in instructions:
            print instruction


if __name__ == '__main__':
    parser = Parser()

    instructions = None
    with open("example/dev.fsdir") as f:
        instructions = parser.parse_s(f.read())
    parser.debug()
