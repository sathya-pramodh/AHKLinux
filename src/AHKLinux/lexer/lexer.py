from base_classes.tokens import Token
from base_classes.position import Position
from error_classes.illegal_char_error import IllegalCharError
from constants import *


class Lexer:
    def __init__(self, text, filename, context):
        self.text = text
        self.pos = Position(filename, 0, 1, 1, text)
        self.context = context
        if self.text == "":
            self.current_char = None
        else:
            self.current_char = self.text[self.pos.idx]

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = (
            self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        )

    def get_previous_char(self, idx):
        return self.text[idx - 1] if idx - 1 >= 0 else None

    def get_next_char(self, idx):
        return self.text[idx + 1] if idx + 1 < len(self.text) else None

    def tokenize(self):
        tokens = []
        if self.text == "":
            return [], None

        while self.current_char is not None:
            if self.current_char in " \t\n":
                self.advance()
                continue

            elif self.current_char == ".":
                tokens.append(Token(T_CONCAT, pos_start=self.pos))

            elif self.current_char == "+":
                tokens.append(Token(T_PLUS, pos_start=self.pos))

            elif self.current_char == "-":
                tokens.append(Token(T_MINUS, pos_start=self.pos))

            elif self.current_char == "*":
                tokens.append(Token(T_MULTIPLY, pos_start=self.pos))

            elif self.current_char == "/":
                tokens.append(Token(T_DIVIDE, pos_start=self.pos))

            elif self.current_char in LETTERS + "@#_$":
                tokens.append(self.make_identifier())
                continue

            elif self.current_char == ":":
                next_char = self.get_next_char(self.pos.idx)
                if next_char is not None and next_char == "=":
                    self.advance()
                else:
                    char = self.current_char
                    return [], IllegalCharError(
                        self.pos, self.pos, "'{}'".format(char), self.context
                    )
                tokens.append(Token(T_ASSIGNMENT, pos_start=self.pos))

            elif self.current_char == "(":
                tokens.append(Token(T_LPAREN, pos_start=self.pos))

            elif self.current_char == ")":
                tokens.append(Token(T_RPAREN, pos_start=self.pos))

            elif self.current_char in DIGITS:
                result, error = self.make_number()
                if error:
                    return [], error
                tokens.append(result)
                continue

            elif self.current_char == '"':
                self.advance()
                pos_start = self.pos.copy()
                value = self.make_string()
                if self.current_char != '"':
                    return [], IllegalCharError(
                        pos_start, self.pos, "Expected '{}'".format('"'), self.context
                    )
                tokens.append(Token(T_STRING, value, pos_start=self.pos))
                self.advance()
                continue

            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(
                    pos_start, self.pos, "'{}'".format(char), self.context
                )
            self.advance()
        return tokens, None

    def make_number(self):
        number_str = ""
        dot_count = 0
        x_count = 0
        char_count = 0
        pos_start = self.pos

        while (
            self.current_char is not None
            and self.current_char != "\n"
            and self.current_char in DIGITS + ".xabcdefABCDEF"
        ):
            if self.current_char == ".":
                next_char = self.get_next_char(self.pos.idx)
                if dot_count == 1 or next_char is None or next_char not in DIGITS:
                    char = self.current_char
                    return None, IllegalCharError(
                        self.pos.copy(), self.pos, "'{}'".format(char), self.context
                    )
                dot_count += 1
                number_str += "."
            elif self.current_char == "x":
                previous_char = self.get_previous_char(self.pos.idx)
                previous_previous_char = self.get_previous_char(self.pos.idx - 1)
                if previous_previous_char is not None:
                    if previous_previous_char in DIGITS + LETTERS:
                        char = self.current_char
                        return None, IllegalCharError(
                            self.pos.copy(), self.pos, "'{}'".format(char), self.context
                        )
                next_char = self.get_next_char(self.pos.idx)
                if (
                    x_count == 1
                    or previous_char != "0"
                    or previous_char is None
                    or next_char is None
                    or next_char not in DIGITS + "abcdefABCDEF"
                ):
                    char = self.current_char
                    return None, IllegalCharError(
                        self.pos.copy(), self.pos, "'{}'".format(char), self.context
                    )
                x_count += 1
                number_str += "x"
            elif self.current_char in "abcdefABCDEF":
                char_count += 1
                number_str += self.current_char
            else:
                number_str += self.current_char
            self.advance()

        if dot_count == 0 and x_count == 0 and char_count == 0:
            return Token(T_DECIMAL, int(number_str), pos_start, self.pos), None
        elif dot_count == 1 and x_count == 0 and char_count == 0:
            return Token(T_FLOAT, float(number_str), pos_start, self.pos), None
        elif dot_count == 0 and x_count == 1:
            return Token(T_HEXADECIMAL, number_str, pos_start, self.pos), None
        else:
            char = self.current_char
            return None, IllegalCharError(
                self.pos.copy(), self.pos, "'{}'".format(char), self.context
            )

    def make_identifier(self):
        identifier_str = ""
        pos_start = self.pos.copy()

        while (
            self.current_char is not None
            and self.current_char in LETTERS + DIGITS + "_#@$"
        ):
            identifier_str += self.current_char
            self.advance()

        tok_type = T_KEYWORD if identifier_str in KEYWORDS else T_IDENTIFIER
        return Token(tok_type, identifier_str, pos_start)

    def make_string(self):
        string_value = ""
        pos_start = self.pos.copy()
        while self.current_char is not None and self.current_char != '"':
            string_value += self.current_char
            self.advance()
        return string_value
