"""
Grammar:
    expression: (KEYWORD:global)* IDENTIFIER ASSIGNMENT expression
              : (KEYWORD:global)* IDENTIFIER
              : term (PLUS|MINUS term)*
              : STRING (DOT STRING)*
              : IDENTIFIER (DOT IDENTIFIER)* (LSQUARE (atom)? RSQUARE)* (ASSIGNMENT expression)*
    term: factor (MULTIPLY|DIVIDE factor)*
    factor: (PLUS|MINUS) factor
          : atom
    atom : DECIMAL|HEXADECIMAL|FLOAT|STRING
         : LPAREN expr RPAREN
         : array-expr
         : associative-array-expr
    array-expr : LSQUARE (expr (COMMA expr)*)? RSQUARE
    associative-array-expr : LCURVE (expression (COMMA expression)*)? RCURVE
"""
from constants import *
from base_classes.nodes import *
from parser.parse_result import ParseResult
from error_classes.invalid_syntax_error import InvalidSyntaxError
from error_classes.unexpected_eol_error import UnexpectedEOLError
from base_classes.tokens import Token


class Parser:
    def __init__(self, tokens, context):
        self.tokens = tokens
        self.tok_idx = 0
        self.context = context
        self.current_tok = self.tokens[self.tok_idx]

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def recede(self):
        if self.tok_idx - 1 >= 0:
            self.tok_idx -= 1
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def get_keys(self, accumulator, res, var_name):
        while self.current_tok.type in (T_DOT, T_LSQUARE):
            if self.current_tok.type == T_DOT:
                op_tok = self.current_tok
                self.advance()
                if self.current_tok.type == T_STRING:
                    accumulator = BinOpNode(
                        accumulator, op_tok, StringNode(self.current_tok)
                    )
                else:
                    accumulator = BinOpNode(
                        accumulator, op_tok, VarAccessNode(self.current_tok)
                    )
                previous_tok = self.current_tok
                self.advance()
                if self.current_tok == previous_tok:
                    if previous_tok.type == T_DOT:
                        return res.failure(
                            UnexpectedEOLError(
                                var_name.pos_start,
                                self.current_tok.pos_start,
                                "Unexpected EOL while reading '{}'.".format(
                                    self.current_tok
                                ),
                                self.context,
                            )
                        )
                    break
            elif self.current_tok.type == T_LSQUARE:
                self.advance()
                if self.current_tok.type == T_RSQUARE:
                    return res.failure(
                        InvalidSyntaxError(
                            var_name.pos_start,
                            self.current_tok.pos_end,
                            "Expected a key inside '[]'.",
                            self.context,
                        )
                    )
                inner_key = res.register(self.atom())
                if res.error:
                    return res
                if isinstance(inner_key, VarAccessNode):
                    return res.failure(
                        InvalidSyntaxError(
                            var_name.pos_start,
                            self.current_tok.pos_end,
                            "Usage of variable names inside '[]' is not allowed.",
                            self.context,
                        )
                    )
                if self.current_tok.type != T_RSQUARE:
                    return res.failure(
                        InvalidSyntaxError(
                            var_name.pos_start,
                            self.current_tok.pos_end,
                            "Expected ']'.",
                            self.context,
                        )
                    )
                previous_tok = self.current_tok
                self.advance()
                if self.current_tok == previous_tok:
                    if previous_tok.type == T_DOT:
                        return res.failure(
                            UnexpectedEOLError(
                                var_name.pos_start,
                                self.current_tok.pos_start,
                                "Unexpected EOL while reading '{}'.".format(
                                    self.current_tok
                                ),
                                self.context,
                            )
                        )
                    break
                accumulator = BinOpNode(
                    accumulator, Token(T_DOT), VarAccessNode(inner_key.tok)
                )
        if self.current_tok.type == T_ASSIGNMENT:
            self.advance()
            value = res.register(self.expression())
            if res.error:
                return res
            return res.success(
                AssociativeArrayAssignNode(
                    accumulator.left_node, accumulator.right_node, value
                )
            )
        return res.success(
            AssociativeArrayAccessNode(accumulator.left_node, accumulator.right_node)
        )

    def parse(self):
        ast = []
        while self.tok_idx < len(self.tokens):
            if self.current_tok is None:
                return [], None
            res = self.expression()
            if res.error:
                return [], res.error
            ast.append(res)
        return ast, None

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            self.advance()
            right = res.register(func())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (T_DECIMAL, T_FLOAT, T_HEXADECIMAL):
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == T_STRING:
            self.advance()
            return res.success(StringNode(tok))

        elif tok.type == T_IDENTIFIER:
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == T_LPAREN:
            self.advance()
            expr = res.register(self.expression())
            if res.error:
                return res
            if self.current_tok.type == T_RPAREN:
                self.advance()
                return res.success(expr)
            return res.failure(
                InvalidSyntaxError(
                    tok.pos_start, tok.pos_end, "Expected ')'.", self.context
                )
            )

        elif tok.type == T_LSQUARE:
            self.advance()
            value_nodes = []
            if self.current_tok.type == T_RSQUARE:
                self.advance()
            else:
                value_nodes.append(res.register(self.expression()))
                if res.error:
                    return res

                while self.current_tok.type == T_COMMA:
                    self.advance()
                    value_nodes.append(res.register(self.expression()))
                    if res.error:
                        return res

                if self.current_tok.type != T_RSQUARE:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected ',' or ']'",
                            self.context,
                        )
                    )
                self.advance()
            return res.success(
                ArrayNode(value_nodes, tok.pos_start, self.current_tok.pos_end)
            )
        elif tok.type == T_LCURVE:
            self.advance()
            value_nodes = {}
            if self.current_tok.type == T_RCURVE:
                self.advance()
            else:
                key_node = res.register(self.expression())
                if res.error:
                    return res
                if self.current_tok.type != T_COLON:
                    return res.failure(
                        InvalidSyntaxError(
                            tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected ':'.",
                            self.context,
                        )
                    )
                self.advance()
                value_node = res.register(self.expression())
                if res.error:
                    return res
                value_nodes[key_node] = value_node
                while self.current_tok.type == T_COMMA:
                    self.advance()
                    key_node = res.register(self.expression())
                    if res.error:
                        return res
                    if self.current_tok.type != T_COLON:
                        return res.failure(
                            InvalidSyntaxError(
                                tok.pos_start,
                                self.current_tok.pos_end,
                                "Expected ':'.",
                                self.context,
                            )
                        )
                    self.advance()
                    value_node = res.register(self.expression())
                    if res.error:
                        return res
                    value_nodes[key_node] = value_node
                if self.current_tok.type != T_RCURVE:
                    return res.failure(
                        InvalidSyntaxError(
                            tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected ',' or '}'.",
                            self.context,
                        )
                    )
                self.advance()

            return res.success(
                AssociativeArrayNode(
                    value_nodes, tok.pos_start, self.current_tok.pos_end
                )
            )

        return res.failure(
            InvalidSyntaxError(
                tok.pos_start,
                tok.pos_end,
                "Expected int, float, hexadecimal, string or an object",
                self.context,
            )
        )

    def factor(self):
        res = ParseResult()
        tok = self.current_tok
        if tok.type in (T_PLUS, T_MINUS):
            self.advance()
            if self.current_tok.type == tok.type:
                return res.failure(
                    InvalidSyntaxError(
                        tok.pos_start,
                        tok.pos_end,
                        "Expected expression after '{}'.".format(tok.type),
                        self.context,
                    )
                )
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))

        return self.atom()

    def term(self):
        return self.bin_op(self.factor, (T_MULTIPLY, T_DIVIDE, T_DOT))

    def expression(self):
        res = ParseResult()
        if self.current_tok.matches(T_KEYWORD, "global"):
            self.advance()
            if self.current_tok.type != T_IDENTIFIER:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected identifier",
                        self.context,
                    )
                )
            var_name = self.current_tok
            self.advance()

            if self.current_tok.type != T_ASSIGNMENT:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected ':='",
                        self.context,
                    )
                )

            self.advance()
            expr = res.register(self.expression())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name, expr, "global"))

        elif self.current_tok.type == T_IDENTIFIER:
            var_name = self.current_tok
            self.advance()

            if self.current_tok.type == T_ASSIGNMENT:
                self.advance()
                expr = res.register(self.expression())
                if res.error:
                    return res
                return res.success(VarAssignNode(var_name, expr))

            elif self.current_tok.type == T_DOT:
                op_tok = self.current_tok
                self.advance()
                if self.current_tok.type == T_STRING:
                    self.recede()
                    self.recede()
                else:
                    accumulator = BinOpNode(
                        VarAccessNode(var_name), op_tok, VarAccessNode(self.current_tok)
                    )
                    self.advance()
                    res = self.get_keys(accumulator, res, var_name)
                    return res
            elif self.current_tok.type == T_LSQUARE:
                self.advance()
                inner_key = res.register(self.atom())
                if res.error:
                    return res
                if isinstance(inner_key, VarAccessNode):
                    return res.failure(
                        InvalidSyntaxError(
                            var_name.pos_start,
                            self.current_tok.pos_end,
                            "Usage of variable names inside '[]' is not allowed.",
                            self.context,
                        )
                    )
                accumulator = BinOpNode(
                    VarAccessNode(var_name),
                    Token(T_DOT),
                    VarAccessNode(inner_key.tok),
                )
                if self.current_tok.type != T_RSQUARE:
                    return res.failure(
                        InvalidSyntaxError(
                            var_name.pos_start,
                            self.current_tok.pos_end,
                            "Expected ']'.",
                            self.context,
                        )
                    )
                self.advance()
                res = self.get_keys(accumulator, res, var_name)
                return res
            elif self.current_tok.type in (
                T_PLUS,
                T_MINUS,
                T_MULTIPLY,
                T_DIVIDE,
                T_COMMA,
                T_LSQUARE,
                T_LCURVE,
                T_COLON,
                T_DOT,
            ):
                self.recede()

        node = res.register(self.bin_op(self.term, (T_PLUS, T_MINUS, T_DOT)))
        if res.error:
            return res
        return res.success(node)
