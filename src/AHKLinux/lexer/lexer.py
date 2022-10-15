from base_classes.context import Context
from base_classes.position import Position
from base_classes.tokens import Token
from constants import *
from error_classes.illegal_char_error import IllegalCharError


class Lexer:
    def __init__(self, text: str, filename: str, context: Context) -> None:
        self.text: str = text
        self.pos: Position = Position(filename, 0, 1, text)
        self.context: Context = context
        if self.text == "":
            self.current_char: str | None = None
        else:
            self.current_char: str | None = self.text[self.pos.idx]

    def advance(self) -> None:
        self.pos.advance(self.current_char)
        self.current_char: str | None = (
            self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        )

    def get_previous_char(self, idx: int) -> str | None:
        return self.text[idx - 1] if idx - 1 >= 0 else None

    def get_next_char(self, idx: int) -> str | None:
        return self.text[idx + 1] if idx + 1 < len(self.text) else None

    def tokenize(self) -> tuple[list[Token], IllegalCharError | None]:
        tokens: list[Token] = [Token(T_SOF, pos_start=self.pos)]
        if self.text == "":
            return [], None

        while self.current_char is not None:
            if self.current_char in " \t":
                self.advance()
                continue

            elif self.current_char == ";":
                self.advance()
                while self.current_char != "\n":
                    self.advance()
                continue

            elif self.current_char == "=":
                tokens.append(Token(T_L_ASSIGNMENT, "=", pos_start=self.pos))
                self.advance()
                string_tok: Token = self.make_u_string()
                tokens.append(string_tok)
                continue

            elif self.current_char == "?":
                tokens.append(Token(T_QUESTION_MARK, "?", pos_start=self.pos))

            elif self.current_char == "%":
                tokens.append(Token(T_PERCENT, "%", pos_start=self.pos))

            elif self.current_char == "\n":
                tokens.append(Token(T_EOL, pos_start=self.pos))

            elif self.current_char == ".":
                tokens.append(Token(T_DOT, ".", pos_start=self.pos))

            elif self.current_char == "+":
                tokens.append(Token(T_PLUS, "+", pos_start=self.pos))

            elif self.current_char == "-":
                tokens.append(Token(T_MINUS, "-", pos_start=self.pos))

            elif self.current_char == "*":
                pos_start: Position = self.pos.copy()
                self.advance()
                if self.current_char == "/":
                    self.advance()
                    tokens.append(
                        Token(
                            T_BCOMMENT_END, "*/", pos_start=pos_start, pos_end=self.pos
                        )
                    )
                    continue
                else:
                    tokens.append(Token(T_MULTIPLY, "*", pos_start=self.pos))
                    continue

            elif self.current_char == "/":
                pos_start: Position = self.pos.copy()
                self.advance()
                if self.current_char == "*":
                    self.advance()
                    tokens.append(
                        Token(
                            T_BCOMMENT_START,
                            "/*",
                            pos_start=pos_start,
                            pos_end=self.pos,
                        )
                    )
                    continue
                else:
                    tokens.append(Token(T_DIVIDE, "/", pos_start=pos_start))
                    continue

            elif self.current_char in LETTERS + "@#_$":
                tokens.append(self.make_identifier())
                continue

            elif self.current_char == ":":
                next_char: str | None = self.get_next_char(self.pos.idx)
                if next_char is not None and next_char == "=":
                    self.advance()
                    tokens.append(Token(T_ASSIGNMENT, ":=", pos_start=self.pos))
                elif next_char is not None:
                    tokens.append(Token(T_COLON, ":", pos_start=self.pos))
                else:
                    char: str | None = self.current_char
                    return [], IllegalCharError(
                        self.pos, self.pos, "'{}'".format(char), self.context
                    )

            elif self.current_char == "(":
                tokens.append(Token(T_LPAREN, "(", pos_start=self.pos))

            elif self.current_char == ")":
                tokens.append(Token(T_RPAREN, ")", pos_start=self.pos))

            elif self.current_char == "[":
                tokens.append(Token(T_LSQUARE, "]", pos_start=self.pos))

            elif self.current_char == "]":
                tokens.append(Token(T_RSQUARE, "]", pos_start=self.pos))

            elif self.current_char == "{":
                tokens.append(Token(T_LCURVE, "{", pos_start=self.pos))

            elif self.current_char == "}":
                tokens.append(Token(T_RCURVE, "}", pos_start=self.pos))

            elif self.current_char == ",":
                tokens.append(Token(T_COMMA, ",", pos_start=self.pos))

            elif self.current_char in DIGITS:
                result, error = self.make_number()
                if error or result is None:
                    return [], error
                tokens.append(result)
                continue

            elif self.current_char == '"':
                self.advance()
                pos_start: Position = self.pos.copy()
                tok: Token = self.make_string()
                if self.current_char != '"':
                    return [], IllegalCharError(
                        pos_start, self.pos, "Expected '{}'".format('"'), self.context
                    )
                tokens.append(tok)

            else:
                tokens.append(Token(T_UNKNOWN, self.current_char, pos_start=self.pos))
            self.advance()
        tokens.append(Token(T_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        number_str: str = ""
        dot_count: int = 0
        x_count: int = 0
        char_count: int = 0
        pos_start: Position = self.pos

        while (
            self.current_char is not None
            and self.current_char != "\n"
            and self.current_char in DIGITS + ".xabcdefABCDEF"
        ):
            if self.current_char == ".":
                next_char: str | None = self.get_next_char(self.pos.idx)
                if dot_count == 1 or next_char is None or next_char not in DIGITS:
                    char: str | None = self.current_char
                    return None, IllegalCharError(
                        self.pos.copy(), self.pos, "'{}'".format(char), self.context
                    )
                dot_count += 1
                number_str += "."
            elif self.current_char == "x":
                previous_char: str | None = self.get_previous_char(self.pos.idx)
                previous_previous_char: str | None = self.get_previous_char(
                    self.pos.idx - 1
                )
                if previous_previous_char is not None:
                    if previous_previous_char in DIGITS + LETTERS:
                        char: str | None = self.current_char
                        return None, IllegalCharError(
                            self.pos.copy(), self.pos, "'{}'".format(char), self.context
                        )
                next_char: str | None = self.get_next_char(self.pos.idx)
                if (
                    x_count == 1
                    or previous_char != "0"
                    or previous_char is None
                    or next_char is None
                    or next_char not in DIGITS + "abcdefABCDEF"
                ):
                    char: str | None = self.current_char
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
            char: str | None = self.current_char
            return None, IllegalCharError(
                self.pos.copy(), self.pos, "'{}'".format(char), self.context
            )

    def make_identifier(self):
        identifier_str: str = ""
        pos_start: Position = self.pos.copy()

        while (
            self.current_char is not None
            and self.current_char in LETTERS + DIGITS + "_#@$"
        ):
            identifier_str += self.current_char
            self.advance()

        tok_type: str = ""
        if identifier_str in KEYWORDS:
            tok_type: str = T_KEYWORD
        elif identifier_str in COMMANDS:
            tok_type: str = T_COMMAND
        elif identifier_str in BOOLEANS:
            tok_type: str = T_BOOLEAN
        else:
            tok_type: str = T_IDENTIFIER
        return Token(tok_type, identifier_str, pos_start)

    def make_string(self):
        string_value: str = ""
        pos_start: Position = self.pos.copy()
        while True:
            if self.current_char is None:
                break
            elif self.current_char == '"':
                next_char: str | None = self.get_next_char(self.pos.idx)
                if next_char == '"':
                    self.advance()
                    self.advance()
                    string_value += '"'
                else:
                    break
            else:
                string_value += self.current_char
                self.advance()
        return Token(T_STRING, string_value, pos_start)

    def make_u_string(self):
        string_value: str = ""
        pos_start: Position = self.pos.copy()
        while True:
            if self.current_char is None or self.current_char == "\n":
                break
            string_value += self.current_char
            self.advance()
        return Token(T_U_STRING, string_value, pos_start)
