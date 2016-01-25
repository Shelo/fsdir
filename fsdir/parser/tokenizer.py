import os
import inspect

from fsdir.parser.indexdata import IndexData, Index


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

        for name, value in inspect.getmembers(Tokenizer,
                lambda a: type(a) == int):
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

        while t_cursor < len(self.source) and \
                self.is_space(self.source[t_cursor]):
            t_cursor += 1

        data.type = self.TYPE_IGNORE
        data.length = t_cursor - self.cursor

    def parse_file_path(self, data):
        """
        Parse entire file path.
        """
        t_cursor = self.cursor + 1

        while t_cursor < len(self.source) and \
                self.source[t_cursor] != self.CHAR_QUOTE:
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

        while t_cursor < len(self.source) and \
                self.source[t_cursor] != self.CHAR_PARENTHESIS_RIGHT:
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

        while t_cursor < len(self.source) and \
                self.source[t_cursor] != self.CHAR_BRACE_RIGHT:
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

        while t_cursor < len(self.source) and \
                self.source[t_cursor] != self.CHAR_NEWLINE:
            t_cursor += 1

        data.type = self.TYPE_COMMENT
        data.length = t_cursor - self.cursor
        data.offset_stop = 1

    def parse_newline(self, data):
        """
        Parse the line break character.
        """
        t_cursor = self.cursor + 1

        while t_cursor < len(self.source) and \
                self.source[t_cursor] == self.CHAR_NEWLINE:
            t_cursor += 1

        data.type = self.TYPE_NEWLINE
        data.length = t_cursor - self.cursor
