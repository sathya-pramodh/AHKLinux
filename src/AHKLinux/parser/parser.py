"""
Grammar:
    statement: return-expr
             : if-expr
             : function-expr(declaration+call)
             : (KEYWORD:global)? IDENTIFIER ASSIGNMENT expression
             : IDENTIFIER (DOT IDENTIFIER)* (LSQUARE (expression)? RSQUARE)* (ASSIGNMENT expression)*
             : IDENTIFIER L_ASSIGNMENT U_STRING
             : command-expr
             : block-comment
    expression: term (PLUS|MINUS term)*
              : STRING (DOT STRING)*
              : term QUESTION_MARK expression COLON expression
    term: factor (MULTIPLY|DIVIDE|KEYWORD:and|or factor)*
    factor: (PLUS|MINUS) factor
          : (KEYWORD:not) expression
          : atom
    atom : DECIMAL|HEXADECIMAL|FLOAT|STRING|BOOLEAN
         : IDENTIFIER
         : function-expr(call only)
         : LPAREN expr RPAREN
         : array-expr
         : associative-array-expr
    array-expr : LSQUARE (expr (COMMA expr)*)? RSQUARE (LSQUARE (expression)? RSQUARE)*
    associative-array-expr : LCURVE (expression (COMMA expression)*)? RCURVE (LSQUARE (expression)? RSQUARE)*
    if-expr : KEYWORD:if expression (KEYWORD:and|or expression)* LCURVE expression (EOL expression)* (KEYWORD:else LCURVE expression (EOL expression)* RCURVE)?
    function-expr : IDENTIFIER LPAREN (expression (COMMA expression)*)? RPAREN (LCURVE (expression (\n expression)*)* RCURVE)?
    return-expr : KEYWORD:return expression
    block-comment : BCOMMENT_START .* BCOMMENT_END
    command-expr : COMMAND (COMMA expression|U_STRING)*
"""
from base_classes.context import Context
from base_classes.nodes import *
from base_classes.tokens import Token
from constants import *
from error_classes.invalid_syntax_error import InvalidSyntaxError
from parser.parse_result import ParseResult


class Parser:
    def __init__(self, tokens: list[Token], context: Context) -> None:
        self.tokens: list[Token] = tokens
        self.tok_idx: int = 0
        self.context: Context = context
        self.current_tok: Token = self.tokens[self.tok_idx]

    def parse(self) -> tuple[list[ParseResult], None]:
        ast: list[ParseResult] = []
        while self.tok_idx < len(self.tokens):
            res: ParseResult = self.statement()
            if res is None or res.error:
                continue
            if res.error:
                return [], res.error
            if res.node is None:
                continue
            ast.append(res)
            if self.current_tok.type == T_EOF:
                break
        return ast, None

    def advance(self) -> None:
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]

    def recede(self) -> None:
        if self.tok_idx - 1 >= 0:
            self.tok_idx -= 1
            self.current_tok = self.tokens[self.tok_idx]

    def get_keys(
        self,
        accumulator: BinOpNode,
        access_method: str,
        res: ParseResult,
        var_name: Token,
        disable_assignment: bool = False,
        disable_access: bool = False,
        disable_dot: bool = False,
    ):
        ops: list[str] = [T_LSQUARE] if disable_dot else [T_DOT, T_LSQUARE]
        while self.current_tok.type in ops:
            if self.current_tok.type == T_DOT:
                if not disable_dot:
                    op_tok: Token = self.current_tok
                    res.register_advancement()
                    self.advance()
                    access_method = T_DOT
                    accumulator = BinOpNode(
                        accumulator, op_tok, ObjectKeyNode(self.current_tok)
                    )
                    res.register_advancement()
                    self.advance()
                else:
                    return res.failure(
                        InvalidSyntaxError(
                            var_name.pos_start,
                            self.current_tok.pos_end,
                            "Cannot use '.' for this operation.",
                            self.context,
                        )
                    )
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
                inner_key: Any = res.register(self.expression())
                if res.error:
                    return res
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
                access_method = T_LSQUARE
                accumulator = BinOpNode(
                    accumulator, Token(T_LSQUARE), ObjectKeyNode(inner_key)
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
            value: Any = res.register(self.expression())
            if res.error:
                return res
            return res.success(
                ObjectAssignNode(
                    accumulator.left_node, accumulator.right_node, access_method, value
                )
            )
        if not disable_access:
            return res.success(
                ObjectAccessNode(
                    accumulator.left_node, accumulator.right_node, access_method
                )
            )
        return res.failure(
            InvalidSyntaxError(
                var_name.pos_start,
                self.current_tok.pos_end,
                "Expected a statement.",
                self.context,
            )
        )

    def ignore_block_comment(self) -> ParseResult:
        res: ParseResult = ParseResult()
        while self.current_tok.type != T_BCOMMENT_END:
            self.advance()
        self.recede()
        previous_tok: Token = self.current_tok
        self.advance()
        self.advance()
        if (previous_tok.type == T_EOL or previous_tok.type == T_SOF) and (
            self.current_tok.type == T_EOL or self.current_tok.type == T_EOF
        ):
            self.advance()
            return res
        else:
            return self.ignore_block_comment()

    def bin_op(self, func: Any, ops: list[str]):
        res = ParseResult()
        left: Any = res.register(func())
        if res.error:
            return res

        while self.current_tok.type in ops:
            op_tok: Token = self.current_tok
            res.register_advancement()
            self.advance()
            right: Any = res.register(func())
            if res.error:
                return res
            left: Any = BinOpNode(left, op_tok, right)

        return res.success(left)

    def get_condition(self) -> ParseResult:
        res: ParseResult = ParseResult()
        left: Any = res.register(self.expression())
        if res.error or left is None:
            return res
        cond: bool = self.current_tok.matches(
            T_KEYWORD, "and"
        ) or self.current_tok.matches(T_KEYWORD, "or")
        while cond:
            op_tok: Token = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type == T_LPAREN:
                res.register_advancement()
                self.advance()
            right: Any = res.register(self.expression())
            if res.error:
                return res
            left: Any = BinOpNode(left, op_tok, right)
            cond: bool = self.current_tok.matches(
                T_KEYWORD, "and"
            ) or self.current_tok.matches(T_KEYWORD, "or")
        return res.success(left)

    def if_expr(self, pos_start: Position) -> ParseResult:
        res: ParseResult = ParseResult()
        condition_node: Any = res.register(self.get_condition())
        if res.error:
            return res
        if self.current_tok.type == T_EOL:
            res.register_advancement()
            self.advance()
        if self.current_tok.type != T_LCURVE:
            return res.failure(
                InvalidSyntaxError(
                    pos_start,
                    self.current_tok.pos_end,
                    "Expected '{'.",
                    self.context,
                )
            )
        res.register_advancement()
        self.advance()
        if_body: list[Any] = []
        if self.current_tok.type == T_EOL:
            res.register_advancement()
            self.advance()
        statement: Any = res.register(self.statement())
        if res.error:
            return res
        if_body.append(statement)
        while True:
            if self.current_tok.type in (T_RCURVE, T_EOF):
                break
            statement: Any = res.register(self.statement())
            if res.error:
                return res
            if_body.append(statement)
        if self.current_tok.type != T_RCURVE:
            return res.failure(
                InvalidSyntaxError(
                    self.current_tok.pos_start,
                    self.current_tok.pos_end,
                    "Expected '}'.",
                    self.context,
                )
            )
        res.register_advancement()
        self.advance()
        if self.current_tok.type == T_EOL:
            res.register_advancement()
            self.advance()
        if self.current_tok.matches(T_KEYWORD, "else"):
            pos_start = self.current_tok.pos_start
            res.register_advancement()
            self.advance()
            if self.current_tok.type == T_EOL:
                res.register_advancement()
                self.advance()
            if self.current_tok.type != T_LCURVE:
                return res.failure(
                    InvalidSyntaxError(
                        pos_start,
                        self.current_tok.pos_end,
                        "Expected '{'.",
                        self.context,
                    )
                )
            res.register_advancement()
            self.advance()
            else_body: list[Any] = []
            if self.current_tok.type == T_EOL:
                res.register_advancement()
                self.advance()
            statement: Any = res.register(self.statement())
            if res.error:
                return res
            else_body.append(statement)
            while True:
                if self.current_tok.type in (T_RCURVE, T_EOF):
                    break
                statement: Any = res.register(self.statement())
                if res.error:
                    return res
                else_body.append(statement)
            if self.current_tok.type != T_RCURVE:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected '}'.",
                        self.context,
                    )
                )
            res.register_advancement()
            self.advance()
            return res.success(IfElseNode(condition_node, if_body, else_body))
        res.register_recession()
        self.recede()
        if self.current_tok.type not in (T_EOL, T_EOF):
            res.register_advancement()
            self.advance()
        return res.success(IfNode(condition_node, if_body))

    def function_expr(
        self, var_name: Token, allow_declaration: bool = True
    ) -> ParseResult:
        res: ParseResult = ParseResult()
        params: list[Any] = []
        if self.current_tok.type == T_RPAREN:
            res.register_advancement()
            self.advance()
        else:
            node: Any = res.register(self.expression())
            params.append(node)
            while self.current_tok.type == T_COMMA:
                res.register_advancement()
                self.advance()
                node: Any = res.register(self.expression())
                if res.error:
                    return res
                params.append(node)
            if self.current_tok.type != T_RPAREN:
                return res.failure(
                    InvalidSyntaxError(
                        var_name.pos_start,
                        self.current_tok.pos_end,
                        "Expected ')'.",
                        self.context,
                    )
                )
            res.register_advancement()
            self.advance()
        if self.current_tok.type == T_EOL:
            res.register_advancement()
            self.advance()
        if self.current_tok.type == T_LCURVE:
            if not allow_declaration:
                return res.failure(
                    InvalidSyntaxError(
                        var_name.pos_start,
                        self.current_tok.pos_end,
                        "Function declaration not allowed here.",
                        self.context,
                    )
                )

            res.register_advancement()
            self.advance()
            if self.current_tok.type == T_EOL:
                res.register_advancement()
                self.advance()
            body: list[Any] = []
            self.context.display_name = var_name.value
            statement: Any = res.register(self.statement())
            if res.error:
                return res
            body.append(statement)
            while True:
                if self.current_tok.type in (T_RCURVE, T_EOF):
                    break
                statement: Any = res.register(self.statement())
                if res.error:
                    return res
                body.append(statement)
            if self.current_tok.type != T_RCURVE:
                return res.failure(
                    InvalidSyntaxError(
                        var_name.pos_start,
                        self.current_tok.pos_end,
                        "Expected '}'.",
                        self.context,
                    )
                )
            res.register_advancement()
            self.advance()
            self.context.display_name = "<module>"
            return res.success(FunctionDeclareNode(var_name, params, body))
        res.register_recession()
        self.recede()
        if self.current_tok.type not in (T_EOL, T_EOF):
            res.register_advancement()
            self.advance()
        return res.success(FunctionCallNode(var_name, params))

    def make_u_string(self, check_commas: bool = True) -> str:
        res: ParseResult = ParseResult()
        string: str = ""
        condition: list[str] = [T_COMMA, T_EOL] if check_commas else [T_EOL]
        while self.current_tok.type not in condition:
            string += str(self.current_tok.value) + " "
            res.register_advancement()
            self.advance()
        return string.strip()

    def atom(self) -> ParseResult:
        res: Any = ParseResult()
        tok: Token = self.current_tok

        if tok.type in (T_DECIMAL, T_FLOAT, T_HEXADECIMAL):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == T_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

        elif tok.type == T_BOOLEAN:
            res.register_advancement()
            self.advance()
            return res.success(BooleanNode(tok))

        elif tok.type == T_IDENTIFIER:
            var_name = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type == T_LPAREN:
                res.register_advancement()
                self.advance()
                res = self.function_expr(var_name, allow_declaration=False)
                return res
            return res.success(VarAccessNode(tok))

        elif tok.type == T_LPAREN:
            res.register_advancement()
            self.advance()
            expr: Any = res.register(self.expression())
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
            value_nodes: list[Any] = []
            if self.current_tok.type == T_RSQUARE:
                res.register_advancement()
                self.advance()
            else:
                value_node: Any = res.register(self.expression())
                if res.error:
                    return res
                value_nodes.append(value_node)

                while self.current_tok.type == T_COMMA:
                    res.register_advancement()
                    self.advance()
                    value_node: Any = res.register(self.expression())
                    if res.error or value_node is None:
                        return res
                    value_nodes.append(value_node)

                if self.current_tok.type != T_RSQUARE:
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected ',' or ']'",
                            self.context,
                        )
                    )
                end_tok: Token = self.current_tok
                res.register_advancement()
                self.advance()
                if self.current_tok.type == T_LSQUARE:
                    res.register_advancement()
                    self.advance()
                    key: Any = res.register(self.expression())
                    if res.error:
                        return res
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
                    accumulator: BinOpNode = BinOpNode(
                        ArrayNode(value_nodes, tok.pos_start, end_tok.pos_end),
                        Token(T_LSQUARE),
                        ObjectKeyNode(key),
                    )
                    access_method: str = T_LSQUARE
                    res: Any = self.get_keys(
                        accumulator,
                        access_method,
                        res,
                        end_tok,
                        disable_assignment=True,
                        disable_dot=True,
                    )
                    return res
            return res.success(
                ArrayNode(value_nodes, tok.pos_start, self.current_tok.pos_end)
            )
        elif tok.type == T_LCURVE:
            res.register_advancement()
            self.advance()
            value_dict: dict[Any, Any] = {}
            if self.current_tok.type == T_RCURVE:
                res.register_advancement()
                self.advance()
            else:
                key_node: Any = res.register(self.expression())
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
                value_node: Any = res.register(self.expression())
                if res.error:
                    return res
                value_dict[key_node] = value_node
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
                    value_dict[key_node] = value_node
                if self.current_tok.type != T_RCURVE:
                    return res.failure(
                        InvalidSyntaxError(
                            tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected ',' or '}'.",
                            self.context,
                        )
                    )
                end_tok: Token = self.current_tok
                res.register_advancement()
                self.advance()
                if self.current_tok.type == T_LSQUARE:
                    res.register_advancement()
                    self.advance()
                    key: Any = res.register(self.expression())
                    if res.error:
                        return res
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
                    accumulator: BinOpNode = BinOpNode(
                        AssociativeArrayNode(
                            value_dict, tok.pos_start, end_tok.pos_end
                        ),
                        Token(T_LSQUARE),
                        ObjectKeyNode(key),
                    )
                    access_method: str = T_LSQUARE
                    res: Any = self.get_keys(
                        accumulator,
                        access_method,
                        res,
                        end_tok,
                        disable_assignment=True,
                    )
                    return res
                if self.current_tok.type == T_DOT:
                    res.register_advancement()
                    self.advance()
                    key: Any = self.current_tok
                    res.register_advancement()
                    self.advance()
                    accumulator: BinOpNode = BinOpNode(
                        AssociativeArrayNode(
                            value_dict, tok.pos_start, end_tok.pos_end
                        ),
                        Token(T_DOT),
                        ObjectKeyNode(key),
                    )
                    access_method: str = T_DOT
                    res: Any = self.get_keys(
                        accumulator,
                        access_method,
                        res,
                        end_tok,
                        disable_assignment=True,
                    )
                    return res
            return res.success(
                AssociativeArrayNode(
                    value_dict, tok.pos_start, self.current_tok.pos_end
                )
            )

        return res.failure(
            InvalidSyntaxError(
                tok.pos_start,
                tok.pos_end,
                "Expected an expression.",
                self.context,
            )
        )

    def factor(self) -> ParseResult:
        res: ParseResult = ParseResult()
        tok: Token = self.current_tok
        if tok.type in (T_PLUS, T_MINUS, T_KEYWORD):
            res.register_advancement()
            self.advance()
            if tok.matches(T_KEYWORD, "not"):
                factor: Any = res.register(self.expression())
                if res.error:
                    return res
            else:
                factor: Any = res.register(self.factor())
                if res.error:
                    return res
            return res.success(UnaryOpNode(tok, factor))

        return self.atom()

    def term(self) -> ParseResult:
        return self.bin_op(self.factor, [T_MULTIPLY, T_DIVIDE, T_DOT, T_KEYWORD])

    def expression(self) -> ParseResult:
        res: Any = ParseResult()

        if self.current_tok.type == T_IDENTIFIER:
            var_name: Token = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type == T_LSQUARE:
                op_tok: Token = self.current_tok
                res.register_advancement()
                self.advance()
                inner_key: Any = res.register(self.expression())
                if res.error or inner_key is None:
                    return res
                accumulator: BinOpNode = BinOpNode(
                    VarAccessNode(var_name), op_tok, ObjectKeyNode(inner_key)
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
                access_method: str = T_LSQUARE
                res: Any = self.get_keys(
                    accumulator,
                    access_method,
                    res,
                    var_name,
                    disable_assignment=True,
                )
                return res

            if self.current_tok.type == T_DOT:
                op_tok: Token = self.current_tok
                res.register_advancement()
                self.advance()
                accumulator: BinOpNode = BinOpNode(
                    VarAccessNode(var_name), op_tok, ObjectKeyNode(self.current_tok)
                )
                res.register_advancement()
                self.advance()
                access_method: str = T_DOT
                res: Any = self.get_keys(
                    accumulator, access_method, res, var_name, disable_assignment=True
                )
                return res

            res.register_recession()
            self.recede()

        node: Any = res.register(
            self.bin_op(self.term, [T_PLUS, T_MINUS, T_DOT, T_KEYWORD])
        )
        if res.error or node is None:
            return res
        if self.current_tok.type == T_QUESTION_MARK:
            res.register_advancement()
            self.advance()
            true_node: Any = res.register(self.expression())
            if res.error:
                return res
            if self.current_tok.type != T_COLON:
                return res.failure(
                    InvalidSyntaxError(
                        node.pos_start,
                        self.current_tok.pos_end,
                        "Expected ':'.",
                        self.context,
                    )
                )
            res.register_advancement()
            self.advance()
            false_node: Any = res.register(self.expression())
            if res.error:
                return res
            return res.success(TernaryOpNode(node, true_node, false_node))
        return res.success(node)

    def statement(self) -> ParseResult:
        res: Any = ParseResult()
        if self.current_tok.matches(T_KEYWORD, "global"):
            res.register_advancement()
            self.advance()
            if self.current_tok.type != T_IDENTIFIER:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected identifier.",
                        self.context,
                    )
                )
            var_name: Token = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != T_ASSIGNMENT:
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected ':='.",
                        self.context,
                    )
                )

            res.register_advancement()
            self.advance()
            expr: Any = res.register(self.expression())
            if res.error:
                return res
            if self.current_tok.type not in (T_EOL, T_EOF):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected end of line or file.",
                        self.context,
                    )
                )
            res.register_advancement()
            self.advance()
            return res.success(VarAssignNode(var_name, expr, "global"))

        elif self.current_tok.matches(T_KEYWORD, "return"):
            res.register_advancement()
            self.advance()
            if self.current_tok.type != T_EOL:
                return_node: Any = res.register(self.expression())
                if res.error:
                    return res
                if self.current_tok.type not in (T_EOL, T_EOF):
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected end of line or file.",
                            self.context,
                        )
                    )
                res.register_advancement()
                self.advance()
                return res.success(ReturnNode(return_node))
            return res.success(ReturnNode(None))

        elif self.current_tok.matches(T_KEYWORD, "if"):
            pos_start: Position = self.current_tok.pos_start
            res.register_advancement()
            self.advance()
            res: Any = self.if_expr(pos_start)
            if self.current_tok.type not in (T_EOL, T_EOF):
                return res.failure(
                    InvalidSyntaxError(
                        self.current_tok.pos_start,
                        self.current_tok.pos_end,
                        "Expected end of line or file.",
                        self.context,
                    )
                )
            res.register_advancement()
            self.advance()
            return res

        elif self.current_tok.type == T_IDENTIFIER:
            var_name: Token = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type == T_LPAREN:
                res.register_advancement()
                self.advance()
                res: Any = self.function_expr(var_name)
                if self.current_tok.type not in (T_EOL, T_EOF):
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected end of line or file.",
                            self.context,
                        )
                    )
                res.register_advancement()
                self.advance()
                return res

            elif self.current_tok.type == T_ASSIGNMENT:
                res.register_advancement()
                self.advance()
                expr: Any = res.register(self.expression())
                if res.error:
                    return res
                if self.current_tok.type not in (T_EOL, T_EOF):
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected end of line or file.",
                            self.context,
                        )
                    )
                res.register_advancement()
                self.advance()
                return res.success(VarAssignNode(var_name, expr))

            elif self.current_tok.type == T_L_ASSIGNMENT:
                res.register_advancement()
                self.advance()
                if self.current_tok.type != T_U_STRING:
                    return res.failure(
                        InvalidSyntaxError(
                            var_name.pos_start,
                            self.current_tok.pos_end,
                            "Expected an unquoted string.",
                            self.context,
                        )
                    )
                value_node: Any = StringNode(self.current_tok, quoted=False)
                res.register_advancement()
                self.advance()
                if self.current_tok.type not in (T_EOL, T_EOF):
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected end of line or file.",
                            self.context,
                        )
                    )
                res.register_advancement()
                self.advance()
                return res.success(VarAssignNode(var_name, value_node))

            elif self.current_tok.type == T_DOT:
                op_tok: Token = self.current_tok
                res.register_advancement()
                self.advance()
                inner_key: Any = self.current_tok
                accumulator: BinOpNode = BinOpNode(
                    VarAccessNode(var_name), op_tok, ObjectKeyNode(inner_key)
                )
                res.register_advancement()
                self.advance()
                access_method: str = T_DOT
                res: Any = self.get_keys(
                    accumulator, access_method, res, var_name, disable_access=True
                )
                if self.current_tok.type not in (T_EOL, T_EOF):
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected end of line or file.",
                            self.context,
                        )
                    )
                res.register_advancement()
                self.advance()
                return res

            elif self.current_tok.type == T_LSQUARE:
                op_tok: Token = self.current_tok
                res.register_advancement()
                self.advance()
                inner_key: Any = res.register(self.expression())
                if res.error or inner_key is None:
                    return res
                accumulator = BinOpNode(VarAccessNode(var_name), op_tok, inner_key)

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
                access_method: str = T_LSQUARE
                res: Any = self.get_keys(
                    accumulator, access_method, res, var_name, disable_access=True
                )
                if self.current_tok.type not in (T_EOL, T_EOF):
                    return res.failure(
                        InvalidSyntaxError(
                            self.current_tok.pos_start,
                            self.current_tok.pos_end,
                            "Expected end of line or file.",
                            self.context,
                        )
                    )
                res.register_advancement()
                self.advance()
                return res
        elif self.current_tok.matches(T_COMMAND, "MsgBox"):
            name: Token = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type == T_PERCENT:
                res.register_advancement()
                self.advance()
                text: str = res.register(self.expression())
                if res.error:
                    return res
                return res.success(CommandNode(name, text=text))
            if self.current_tok.type == T_COMMA:
                res.register_advancement()
                self.advance()
                if self.current_tok.type not in (T_DECIMAL, T_HEXADECIMAL):
                    return res.failure(
                        InvalidSyntaxError(
                            name.pos_start,
                            self.current_tok.pos_end,
                            "Expected a decimal or hexadecimal for an option.",
                            self.context,
                        )
                    )
                option: NumberNode = NumberNode(self.current_tok)
                res.register_advancement()
                self.advance()
                if self.current_tok.type != T_COMMA:
                    return res.failure(
                        InvalidSyntaxError(
                            name.pos_start,
                            self.current_tok.pos_end,
                            "Expected ','.",
                            self.context,
                        )
                    )
                res.register_advancement()
                self.advance()
                if self.current_tok.type == T_COMMA:
                    res.register_advancement()
                    self.advance()
                    text = self.make_u_string(check_commas=True)
                    if self.current_tok.type == T_COMMA:
                        res.register_advancement()
                        self.advance()
                        if self.current_tok.type not in (T_DECIMAL, T_HEXADECIMAL):
                            return res.failure(
                                InvalidSyntaxError(
                                    name.pos_start,
                                    self.current_tok.pos_end,
                                    "Expected a decimal or a hexadecimal for the timeout option.",
                                    self.context,
                                )
                            )
                        timeout: NumberNode = NumberNode(self.current_tok)
                        res.register_advancement()
                        self.advance()
                        if self.current_tok.type not in (T_EOL, T_EOF):
                            return res.failure(
                                InvalidSyntaxError(
                                    name.pos_start,
                                    self.current_tok.pos_end,
                                    "Expected end of line or file.",
                                    self.context,
                                )
                            )
                        return res.success(
                            CommandNode(name, option=option, text=text, timeout=timeout)
                        )
                    if self.current_tok.type not in (T_EOL, T_EOF):
                        return res.failure(
                            InvalidSyntaxError(
                                name.pos_start,
                                self.current_tok.pos_end,
                                "Expected end of line or file.",
                                self.context,
                            )
                        )
                    return res.success(CommandNode(name, option=option, text=text))
                else:
                    title: Any = self.make_u_string()
                    if self.current_tok.type != T_COMMA:
                        return res.failure(
                            InvalidSyntaxError(
                                name.pos_start,
                                self.current_tok.pos_end,
                                "Expected ','.",
                                self.context,
                            )
                        )
                    res.register_advancement()
                    self.advance()
                    text: str = self.make_u_string()
                    if self.current_tok.type == T_COMMA:
                        res.register_advancement()
                        self.advance()
                        if self.current_tok.type == T_PERCENT:
                            res.register_advancement()
                            self.advance()
                            timeout = res.register(self.expression())
                            if res.error:
                                return res
                            if self.current_tok.type not in (T_EOL, T_EOF):
                                return res.failure(
                                    InvalidSyntaxError(
                                        name.pos_start,
                                        self.current_tok.pos_end,
                                        "Expected end of line or file.",
                                        self.context,
                                    )
                                )
                            return res.success(
                                CommandNode(
                                    name,
                                    option=option,
                                    title=title,
                                    text=text,
                                    timeout=timeout,
                                )
                            )
                        if self.current_tok.type not in (T_DECIMAL, T_HEXADECIMAL):
                            return res.failure(
                                InvalidSyntaxError(
                                    name.pos_start,
                                    self.current_tok.pos_end,
                                    "Expected a number or a hexadecimal for a timeout.",
                                    self.context,
                                )
                            )
                        timeout: NumberNode = NumberNode(self.current_tok)
                        res.register_advancement()
                        self.advance()
                        if self.current_tok.type not in (T_EOL, T_EOF):
                            return res.failure(
                                InvalidSyntaxError(
                                    name.pos_start,
                                    self.current_tok.pos_end,
                                    "Expected end of line or file.",
                                    self.context,
                                )
                            )
                        return res.success(
                            CommandNode(
                                name,
                                option=option,
                                title=title,
                                text=text,
                                timeout=timeout,
                            )
                        )
                    if self.current_tok.type not in (T_EOL, T_EOF):
                        return res.failure(
                            InvalidSyntaxError(
                                name.pos_start,
                                self.current_tok.pos_end,
                                "Expected end of line or file.",
                                self.context,
                            )
                        )
                    res.register_advancement()
                    self.advance()
                    return res.success(
                        CommandNode(name, option=option, title=title, text=text)
                    )
            pos_start: Position = self.current_tok.pos_start
            text: str = self.make_u_string(check_commas=False)
            node: StringNode = StringNode(
                Token(T_STRING, text, pos_start=pos_start), quoted=False
            )
            if self.current_tok.type not in (T_EOL, T_EOF):
                return res.failure(
                    InvalidSyntaxError(
                        name.pos_start,
                        self.current_tok.pos_end,
                        "Expected end of line or file.",
                        self.context,
                    )
                )
            res.register_advancement()
            self.advance()
            return res.success(CommandNode(name, text=node))

        elif self.current_tok.type == T_BCOMMENT_START:
            self.recede()
            previous_tok: Token = self.current_tok
            self.advance()
            self.advance()
            if (previous_tok.type == T_EOL or previous_tok.type == T_SOF) and (
                self.current_tok.type == T_EOL or self.current_tok.type == T_EOF
            ):
                self.advance()
                return self.ignore_block_comment()

        elif self.current_tok.type in (T_EOL, T_EOF, T_SOF):
            res.register_advancement()
            self.advance()
            return res

        return res.failure(
            InvalidSyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_start,
                "Expected a statement.",
                self.context,
            )
        )
