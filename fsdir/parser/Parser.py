class Token(object):
    def __init__(self, position=0, length=0, type=0):
        self.position = position
        self.length = length
        self.type = type


class TokenData(object):
    def __init__(self, length=0, type_=0, offset_start=0, offset_stop=0):
        self.length = length
        self.type = type_
        self.offset_start = offset_start
        self.offset_stop = offset_stop


class Tokenizer(object):
    TYPE_IGNORE = 0
    TYPE_IDENTIFIER = 1
    TYPE_FILE_PATH = 2
    TYPE_PARAMETER = 3
    TYPE_BLANK_SPACE = 4
    TYPE_TEXT_PARAMETER = 5

    CHAR_QUOTE = '\''
    CHAR_PARENTHESIS_LEFT = '('
    CHAR_PARENTHESIS_RIGHT = ')'
    CHAR_BRACE_LEFT = '{'
    CHAR_BRACE_RIGHT = '}'

    def __init__(self, source):
        self.source = source
        self.cursor = 0
        self.tokens = []

        self.process()

    def process(self):
        while self.cursor < len(self.source):
            self.process_command(self.source[self.cursor])

    def process_command(self, c):
        data = TokenData()

        if c.isupper():
            self.parse_identifier(data)
        elif c.isspace():
            self.parse_space(data)
        elif c == self.CHAR_QUOTE:
            self.parse_file_path(data)
        elif c == self.CHAR_PARENTHESIS_LEFT:
            self.parse_parameter(data)
        elif c == self.CHAR_BRACE_LEFT:
            self.parse_text_param(data)
        else:
            raise ValueError("Wrong syntax: " + self.source[self.cursor:])

        self.cursor += data.offset_start

        if data.type != self.TYPE_IGNORE:
            # do not include tokens that can be ignored.
            self.tokens.append(Token(self.cursor, data.length, data.type))

        self.cursor += data.length + data.offset_stop

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

        while t_cursor < len(self.source) and self.source[t_cursor].isspace():
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
        t_cursor = self.cursor + 1

        while t_cursor < len(self.source) and self.source[t_cursor] != self.CHAR_PARENTHESIS_RIGHT:
            t_cursor += 1

        data.type = self.TYPE_PARAMETER
        data.length = t_cursor - self.cursor - 1
        data.offset_start = 1
        data.offset_stop = 1

    def parse_text_param(self, data):
        t_cursor = self.cursor + 1

        while t_cursor < len(self.source) and self.source[t_cursor] != self.CHAR_BRACE_RIGHT:
            t_cursor += 1

        data.type = self.TYPE_TEXT_PARAMETER
        data.length = t_cursor - self.cursor - 1
        data.offset_start = 1
        data.offset_stop = 1


class ElementParser(object):
    pass


class Parser(object):
    def __init__(self):
        self.tokens = None
        self.source = None

    def parse_s(self, source):
        self.source = source

        tokenizer = Tokenizer(source)
        self.tokens = tokenizer.tokens

    def debug(self):
        for token in self.tokens:
            print self.source[token.position:token.position + token.length]

if __name__ == '__main__':
    parser = Parser()
    parser.parse_s("FILE 'example/target/ch_file.md' 'example/target/dummy_file.md' CHMOD {Hello}")
    parser.debug()
