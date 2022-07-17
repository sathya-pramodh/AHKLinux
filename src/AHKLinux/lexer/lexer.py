from base_classes.tokens import Token
from base_classes.token_stream import TokenStream
from error_classes.unexpected_token_error import UnexpectedTokenError
import re


class Lexer:
    """
    Custom lexer class for AutoHotKey.
    """

    def __init__(self, contents):
        self._contents = contents
        self._token_list = []

    def lex(self):
        self._tokenize()
        return TokenStream(self._token_list)

    def _tokenize(self):
        self._read_line_no = 1
        self._contents = self._contents.strip()
        for line in self._contents.split("\n"):
            assignment_match = re.search(r".+:=.+", line)
            only_comment_match = re.search(r"^;.+$", line)
            if assignment_match:
                self._handle_assigment_line(line)
            if only_comment_match:
                self._classify_token(line)

            self._read_line_no += 1

    def _classify_token(self, token):
        if token == "global":
            self._token_list.append(Token("GLOBAL", token))
            return

        if token == "true" or token == "false":
            self._token_list.append(Token("BOOLEAN", token))
            return

        if token == ":=":
            self._token_list.append(Token("EQUALS", token))
            return

        string_match = re.search(r'^".+"$', token)
        string_error_check = re.search(r'^""+.+"+"$', token) or token.count('"') == 1
        if string_match and not string_error_check:
            self._token_list.append(Token("STRING", token))
            return

        integer_match = re.search(r"^\d+[^x]", token)
        if integer_match:
            if "." in token:
                self._token_list.append(Token("FLOATING", token))
            else:
                self._token_list.append(Token("DECIMAL", token))
            return

        hex_match = re.search(r"^0x[0-9]+", token)
        if hex_match and "." not in token:
            self._token_list.append(Token("HEXADECIMAL", token))
            return

        variable_match = re.search(r"^[a-zA-z_][a-zA-Z0-9_]*", token)
        if variable_match:
            self._token_list.append(Token("VARIABLE", token))
            return

        comment_match = re.search(r"^;.+", token)
        if comment_match:
            self._token_list.append(Token("SINGLE_COMMENT", token))
            return

        raise UnexpectedTokenError(
            "Unexpected Token '{}' at line {}.".format(token, self._read_line_no)
        )

    def _handle_assigment_line(self, line):
        left, right = line.split(":=")
        variable_match = re.search(r"(global )?[a-zA-z_][a-zA-Z0-9_]*[^:=]", left)
        right_match = re.search(r".+\s*;*\s*.*[^:=]", right)
        if variable_match:
            left.replace(" ", "")
            if "global " in left:
                if left.count("global ") > 1:
                    raise UnexpectedTokenError(
                        "Unexpected Token in '{}' in line {}".format(
                            left, self._read_line_no
                        )
                    )
                left = left.replace("global ", "")
                self._classify_token("global")
                self._classify_token(left)
            else:
                self._classify_token(left)
        else:
            raise UnexpectedTokenError(
                "Unexpected Token in '{}' in line {}".format(left, self._read_line_no)
            )

        self._classify_token(":=")

        if right_match:
            if ";" in right:
                value, comment = right.split(";")
                self._classify_token(value.strip())
                self._classify_token(";" + comment.strip())
            else:
                self._classify_token(right.strip())
        else:
            raise UnexpectedTokenError(
                "Unexpected Token in '{}' in line {}".format(left, self._read_line_no)
            )
