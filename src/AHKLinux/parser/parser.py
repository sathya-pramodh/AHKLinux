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
         : EOL
    array-expr : LSQUARE (expr (COMMA expr)*)? RSQUARE (LSQUARE (atom)? RSQUARE)*
    associative-array-expr : LCURVE (expression (COMMA expression)*)? RCURVE (LSQUARE (atom)? RSQUARE)*
"""
from constants import *
from base_classes.nodes import *
from parser.parse_result import ParseResult
from error_classes.invalid_syntax_error import InvalidSyntaxError
from base_classes.tokens import Token


class Parser:
    def __init__(self, tokens, context):
        self.tokens = tokens
        self.tok_idx = 0
        self.context = context
        self.current_tok = self.tokens[self.tok_idx]

    def parse(self):
        ast = []
        while self.tok_idx < len(self.tokens):
            res = self.expression()
            if res.error:
                return [], res.error
            ast.append(res)
            if self.current_tok.type == T_EOL:
                break
        return ast, None

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]

    def recede(self):
        if self.tok_idx - 1 >= 0:
            self.tok_idx -= 1
            self.current_tok = self.tokens[self.tok_idx]

    def get_keys(self, accumulator, res, var_name, disable_assignment=False):
        while self.current_tok.type in (T_DOT, T_LSQUARE):
            if self.current_tok.type == T_DOT:
                op_tok = self.current_tok
                res.register_advancement()
                self.advance()
                if self.current_tok.type == T_STRING:
                    accumulator = BinOpNode(
                        accumulator, op_tok, StringNode(self.current_tok)
                    )
                else:
                    accumulator = BinOpNode(
                        accumulator, op_tok, VarAccessNode(self.current_tok)
                    )
                res.register_advancement()
                self.advance()
            elif self.current_tok.type == T_LSQUARE:
                res.register_advancement()
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
                inner_key = res.register(self.expression())
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
                res.register_advancement()
                self.advance()
                accumulator = BinOpNode(
                    accumulator, Token(T_DOT), VarAccessNode(inner_key.tok)
                )
        if self.current_tok.type == T_ASSIGNMENT:
            if disable_assignment:
                return res.failure(
                    InvalidSyntaxError(
                        var_name.pos_start,
                        self.current_tok.pos_end,
                        "Cannot assign this type to anything.",
                        self.context,
                    )
                )
            res.register_advancement()
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

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register_advancement()
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
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == T_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

        elif tok.type == T_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == T_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expression())
            if res.error:
                return res
            if self.current_tok.type == T_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            return res.failure(
                InvalidSyntaxError(
                    tok.pos_start, tok.pos_end, "Expected ')'.", self.context
                )
            )

        elif tok.type == T_LSQUARE:
            res.register_advancement()
            self.advance()
            value_nodes = []
            if self.current_tok.type == T_RSQUARE:
                res.register_advancement()
                self.advance()
            else:
                value_nodes.append(res.register(self.expression()))
                if res.error:
                    return res

                while self.current_tok.type == T_COMMA:
                    res.register_advancement()
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
                end_tok = self.current_tok
                res.register_advancement()
                self.advance()
                if self.current_tok.type == T_LSQUARE:
                    res.register_advancement()
                    self.advance()
                    key = self.current_tok
                    res.register_advancement()
                    self.advance()
                    if self.current_tok.type != T_RSQUARE:
                        return res.failure(
                            InvalidSyntaxError(
                                tok.pos_start,
                                self.current_tok.pos_end,
                                "Expected ']'.",
                                self.context,
                            )
                        )
                    res.register_advancement()
                    self.advance()
                    accumulator = BinOpNode(
                        ArrayNode(value_nodes, tok.pos_start, end_tok.pos_end),
                        Token(T_DOT),
                        VarAccessNode(key),
                    )
                    res = self.get_keys(
                        accumulator, res, end_tok, disable_assignment=True
                    )
                    return res
            return res.success(
                ArrayNode(value_nodes, tok.pos_start, self.current_tok.pos_end)
            )
        elif tok.type == T_LCURVE:
            res.register_advancement()
            self.advance()
            value_nodes = {}
            if self.current_tok.type == T_RCURVE:
                res.register_advancement()
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
                res.register_advancement()
                self.advance()
                value_node = res.register(self.expression())
                if res.error:
                    return res
                value_nodes[key_node] = value_node
                while self.current_tok.type == T_COMMA:
                    res.register_advancement()
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
                    res.register_advancement()
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
                end_tok = self.current_tok
                res.register_advancement()
                self.advance()
                if self.current_tok.type == T_LSQUARE:
                    res.register_advancement()
                    self.advance()
                    key = self.current_tok
                    res.register_advancement()
                    self.advance()
                    if self.current_tok.type != T_RSQUARE:
                        return res.failure(
                            InvalidSyntaxError(
                                tok.pos_start,
                                end_tok.pos_end,
                                "Expected ']'.",
                                self.context,
                            )
                        )
                    res.register_advancement()
                    self.advance()
                    accumulator = BinOpNode(
                        AssociativeArrayNode(
                            value_nodes, tok.pos_start, end_tok.pos_end
                        ),
                        Token(T_DOT),
                        VarAccessNode(key),
                    )
                    res = self.get_keys(
                        accumulator, res, end_tok, disable_assignment=True
                    )
                    return res
                if self.current_tok.type == T_DOT:
                    res.register_advancement()
                    self.advance()
                    key = self.current_tok
                    res.register_advancement()
                    self.advance()
                    accumulator = BinOpNode(
                        AssociativeArrayNode(
                            value_nodes, tok.pos_start, end_tok.pos_end
                        ),
                        Token(T_DOT),
                        VarAccessNode(key),
                    )
                    res = self.get_keys(
                        accumulator, res, end_tok, disable_assignment=True
                    )
                    return res
            return res.success(
                AssociativeArrayNode(
                    value_nodes, tok.pos_start, self.current_tok.pos_end
                )
            )
        elif tok.type == T_EOL:
            return res

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
            res.register_advancement()
            self.advance()
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
            res.register_advancement()
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
            res.register_advancement()
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

            res.register_advancement()
            self.advance()
            expr = res.register(self.expression())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name, expr, "global"))

        elif self.current_tok.type == T_IDENTIFIER:
            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type == T_ASSIGNMENT:
                res.register_advancement()
                self.advance()
                expr = res.register(self.expression())
                if res.error:
                    return res
                return res.success(VarAssignNode(var_name, expr))

            elif self.current_tok.type == T_DOT:
                op_tok = self.current_tok
                res.register_advancement()
                self.advance()
                if self.current_tok.type == T_STRING:
                    res.register_recession()
                    self.recede()
                    res.register_recession()
                    self.recede()
                else:
                    accumulator = BinOpNode(
                        VarAccessNode(var_name), op_tok, VarAccessNode(self.current_tok)
                    )
                    res.register_advancement()
                    self.advance()
                    res = self.get_keys(accumulator, res, var_name)
                    return res
            elif self.current_tok.type == T_LSQUARE:
                res.register_advancement()
                self.advance()
                inner_key = res.register(self.expression())
                if res.error or inner_key is None:
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
                res.register_advancement()
                self.advance()
                res = self.get_keys(accumulator, res, var_name)
                return res
            elif self.current_tok.type in (
                T_PLUS,
                T_MINUS,
                T_MULTIPLY,
                T_DIVIDE,
                T_DOT,
            ):
                res.register_recession()
                self.recede()

            res.register_recession()
            self.recede()

        elif self.current_tok.type in (T_LSQUARE, T_LCURVE, T_IDENTIFIER):
            node = res.register(self.atom())
            if res.error:
                return res
            return res.success(node)

        elif self.current_tok.type == T_EOL:
            return res
        node = res.register(self.bin_op(self.term, (T_PLUS, T_MINUS, T_DOT)))
        if res.error:
            return res
        return res.success(node)
