"""
Grammar:
    expression: (KEYWORD:global)* IDENTIFIER ASSIGNMENT expression
              : (KEYWORD:global)* IDENTIFIER
              : term (PLUS|MINUS term)*
              : term:STRING (DOT term:STRING)*
    term: factor (MULTIPLY|DIVIDE factor)*
        : factor:STRING (DOT factor:STRING)*
    factor: (PLUS|MINUS) factor
          : atom
    atom : DECIMAL|HEXADECIMAL|FLOAT|STRING|ARRAY
         : LPAREN expr RPAREN
         : array-expr
         : object-expr
    array-expr : LSQUARE (expr (COMMA expr)*)? RSQUARE
    object-expr : LCURVE (expr COLON expr (COMMA expr COLON expr)*)? RCURVE
"""
from constants import *
from base_classes.nodes import *
from parser.parse_result import ParseResult
from error_classes.invalid_syntax_error import InvalidSyntaxError


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
        self.tok_idx -= 1
        if self.tok_idx >= 0:
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

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
            elif self.current_tok.type in (
                T_PLUS,
                T_MINUS,
                T_MULTIPLY,
                T_DIVIDE,
                T_DOT,
                T_COMMA,
                T_RSQUARE,
                T_RCURVE,
                T_COLON,
            ):
                self.recede()

        node = res.register(self.bin_op(self.term, (T_PLUS, T_MINUS, T_DOT)))
        if res.error:
            return res
        return res.success(node)

    def term(self):
        return self.bin_op(self.factor, (T_MULTIPLY, T_DIVIDE, T_DOT))

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
                while self.current_tok.type != T_RCURVE:
                    key = res.register(self.expression())
                    if res.error:
                        return res

                    if self.current_tok.type != T_COLON:
                        return res.failure(
                            InvalidSyntaxError(
                                self.current_tok.pos_start,
                                self.current_tok.pos_end,
                                "Expected ':'",
                                self.context,
                            )
                        )
                    self.advance()
                    value = res.register(self.expression())
                    value_nodes[key] = value
                    if self.current_tok.type == T_COMMA:
                        self.advance()
                    elif self.current_tok.type != T_RCURVE:
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
                ObjectNode(value_nodes, tok.pos_start, self.current_tok.pos_end)
            )

        return res.failure(
            InvalidSyntaxError(
                tok.pos_start,
                tok.pos_end,
                "Expected int, float, hexadecimal, string, array or an object",
                self.context,
            )
        )
