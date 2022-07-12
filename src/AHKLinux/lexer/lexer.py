from base_classes.tokens import Token
import re


class Lexer:
    """
    Custom lexer class for AutoHotKey.
    """

    def __init__(self, contents):
        self._contents = contents
        self._token_stream = []

    def lex(self):
        self._tokenize()
        return self._token_stream

    def _tokenize(self):
        token = ""
        for line in self._contents.split("\n"):
            line += " "
            end_of_line = len(line) - 1
            pos = 0
            is_comment = False
            is_string = False
            for char in line:
                if char == " " and not is_string:
                    if pos == end_of_line or not is_comment:
                        self._classify_token(token)
                        token = ""
                    else:
                        token += char
                elif char == '"':
                    is_string = not is_string
                    token += char
                elif char == ";":
                    is_comment = True
                    token += char
                else:
                    token += char
                pos += 1

    def _classify_token(self, token):
        if token == "global":
            self._token_stream.append(Token("GLOBAL", token))
            return

        if token == "true" or token == "false":
            self._token_stream.append(Token("BOOLEAN", token))
            return

        if token == ":=":
            self._token_stream.append(Token("EQUALS", token))
            return

        string_match = re.search(r'^".+"$', token)
        if string_match:
            self._token_stream.append(Token("STRING", token))
            return

        integer_match = re.search(r"^\d+[^x]", token)
        if integer_match:
            if "." in token:
                self._token_stream.append(Token("FLOATING", token))
            else:
                self._token_stream.append(Token("DECIMAL", token))
            return

        hex_match = re.search(r"^0x[0-9]+", token)
        if hex_match and "." not in token:
            self._token_stream.append(Token("HEXADECIMAL", token))
            return

        variable_match = re.search(r"^[a-zA-Z_]+", token)
        if variable_match:
            self._token_stream.append(Token("VARIABLE", token))
            return

        comment_match = re.search(r"^;.+", token)
        if comment_match:
            self._token_stream.append(Token("SINGLE_COMMENT", token))
            return
