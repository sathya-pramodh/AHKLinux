from typing import Any

from base_classes.position import Position
from base_classes.tokens import Token
from constants import T_DOT


class NumberNode:
    def __init__(self, tok: Token) -> None:
        self.tok: Token = tok
        self.pos_start: Position = self.tok.pos_start
        self.pos_end: Position = self.tok.pos_end

    def __repr__(self) -> str:
        return f"{self.tok}"


class StringNode:
    def __init__(self, tok: Token, quoted: bool = True) -> None:
        self.tok: Token = tok
        self.quoted: bool = quoted
        self.pos_start: Position = self.tok.pos_start
        self.pos_end: Position = self.tok.pos_end

    def __repr__(self) -> str:
        return f"{self.tok}"


class BooleanNode:
    def __init__(self, tok: Token) -> None:
        self.tok: Token = tok
        self.pos_start: Position = self.tok.pos_start
        self.pos_end: Position = self.tok.pos_end

    def __repr__(self) -> str:
        return f"{self.tok}"


class ArrayNode:
    def __init__(
        self, value_list: list[Any], pos_start: Position, pos_end: Position
    ) -> None:
        self.value_list: list[Any] = value_list
        self.pos_start: Position = pos_start
        self.pos_end: Position = pos_end

    def __repr__(self) -> str:
        return f"{self.value_list}"


class AssociativeArrayNode:
    def __init__(
        self, value_dict: dict[Any, Any], pos_start: Position, pos_end: Position
    ) -> None:
        self.value_dict: dict[Any, Any] = value_dict
        self.pos_start: Position = pos_start
        self.pos_end: Position = pos_end

    def __repr__(self) -> str:
        return f"{self.value_dict}"


class BinOpNode:
    def __init__(self, left_node: Any, op_tok: Token, right_node: Any) -> None:
        self.left_node: Any = left_node
        self.op_tok: Token = op_tok
        self.right_node: Any = right_node
        self.pos_start: Position = self.left_node.pos_start
        self.pos_end: Position = self.right_node.pos_end

    def __repr__(self) -> str:
        if self.op_tok.type == T_DOT:
            return f"{self.left_node}.{self.right_node}"
        return f"{self.left_node} {self.op_tok} {self.right_node}"


class UnaryOpNode:
    def __init__(self, op_tok: Token, node: Any) -> None:
        self.op_tok: Token = op_tok
        self.node: Any = node
        self.pos_start: Position = self.op_tok.pos_start
        self.pos_end: Position = self.node.pos_end

    def __repr__(self) -> str:
        return f"({self.op_tok}, {self.node})"


class TernaryOpNode:
    def __init__(self, condition_node: Any, true_node: Any, false_node: Any) -> None:
        self.condition_node: Any = condition_node
        self.true_node: Any = true_node
        self.false_node: Any = false_node
        self.pos_start: Position = self.condition_node.pos_start
        self.pos_end: Position = self.false_node.pos_end

    def __repr__(self) -> str:
        return f"{self.condition_node} ? {self.true_node}:{self.false_node}"


class VarAssignNode:
    def __init__(self, var_name: Token, value_node: Any, scope: str = "local") -> None:
        self.var_name: Token = var_name
        self.value_node: Any = value_node
        self.scope: str = scope

        self.pos_start: Position = self.var_name.pos_start
        self.pos_end: Position = self.value_node.pos_end

    def __repr__(self) -> str:
        return f"{self.var_name}:{self.value_node}"


class L_VarAssignNode:
    def __init__(self, var_name: Token, string_node: Any, var_nodes: list[Any]) -> None:
        self.var_name: Token = var_name
        self.string_node: Any = string_node
        self.var_nodes: list[Any] = var_nodes
        self.pos_start: Position = self.var_name.pos_start
        self.pos_end: Position = self.var_name.pos_end

    def __repr__(self) -> str:
        return f"{self.var_name}:{self.string_node}"


class VarAccessNode:
    def __init__(self, var_name_tok: Token) -> None:
        self.var_name_tok: Token = var_name_tok
        self.pos_start: Position = self.var_name_tok.pos_start
        self.pos_end: Position = self.var_name_tok.pos_end

    def __repr__(self) -> str:
        return f"{self.var_name_tok}"


class ObjectAssignNode:
    def __init__(
        self, access_node: Any, key: Any, access_method: str, value_node: Any
    ) -> None:
        self.access_node: Any = access_node
        self.key: Any = key
        self.access_method: str = access_method
        self.value_node: Any = value_node
        self.pos_start: Position = self.access_node.pos_start
        self.pos_end: Position = self.access_node.pos_end

    def __repr__(self) -> str:
        return f"{self.access_node}.{self.key}:{self.value_node}"


class ObjectAccessNode:
    def __init__(self, access_node: Any, key: Any, access_method: Any) -> None:
        self.access_node: Any = access_node
        self.key: Any = key
        self.access_method: Any = access_method
        self.pos_start: Position = self.access_node.pos_start
        self.pos_end: Position = self.access_node.pos_end

    def __repr__(self) -> str:
        return f"{self.access_node} {self.access_method} {self.key}"


class ObjectKeyNode:
    def __init__(self, node: Any) -> None:
        self.node: Any = node
        if isinstance(self.node, Token):
            self.name: Any | None = self.node.value
        elif isinstance(self.node, UnaryOpNode) or isinstance(self.node, BinOpNode):
            self.name: Any | None = None
        else:
            self.name: Any | None = self.node.tok.value
        self.pos_start: Position = self.node.pos_start
        self.pos_end: Position = self.node.pos_end

    def __repr__(self) -> str:
        return f"{self.node}"


class IfNode:
    def __init__(self, condition_node: Any, if_body: list[Any]) -> None:
        self.condition_node: Any = condition_node
        self.if_body: list[Any] = if_body
        self.pos_start: Position = self.condition_node.pos_start
        self.pos_end: Position = (
            self.if_body[-1].pos_end
            if self.if_body != []
            else self.condition_node.pos_end
        )

    def __repr__(self) -> str:
        return f"if {self.condition_node} then {self.if_body}"


class IfElseNode:
    def __init__(
        self, condition_node: Any, if_body: list[Any], else_body: list[Any]
    ) -> None:
        self.condition_node: Any = condition_node
        self.if_body: list[Any] = if_body
        self.else_body: list[Any] = else_body
        self.pos_start: Position = self.condition_node.pos_start
        if self.else_body != []:
            self.pos_end: Position = self.else_body[-1].pos_end
        elif self.if_body != []:
            self.pos_end: Position = self.if_body[-1].pos_end
        else:
            self.pos_end: Position = self.condition_node.pos_end

    def __repr__(self) -> str:
        return f"if {self.condition_node} then {self.if_body} else {self.else_body}"


class FunctionDeclareNode:
    def __init__(self, name: Token, parameters: list[Any], body: list[Any]) -> None:
        self.name: Token = name
        self.parameters: list[Any] = parameters
        self.body: list[Any] = body
        self.pos_start: Position = name.pos_start
        self.pos_end: Position = (
            self.body[-1].pos_end
            if self.body[-1] is not None
            else self.body[-2].pos_end
        )

    def __repr__(self) -> str:
        return r"{}({}){{}}".format(self.name, self.parameters, self.body)


class FunctionCallNode:
    def __init__(self, name: Token, parameters: list[Any]) -> None:
        self.name: Token = name
        self.parameters: list[Any] = parameters
        self.pos_start: Position = name.pos_start
        self.pos_end: Position = (
            self.parameters[-1].pos_end if self.parameters != [] else name.pos_end
        )

    def __repr__(self) -> str:
        return r"{}({})".format(self.name, self.parameters)


class ReturnNode:
    def __init__(self, node: Any) -> None:
        self.node: Any = node
        self.pos_start: Position | None = (
            self.node.pos_start if self.node is not None else None
        )
        self.pos_end: Position | None = (
            self.node.pos_end if self.node is not None else None
        )

    def __repr__(self) -> str:
        return f"return {self.node}"


class CommandNode:
    def __init__(self, name: Token, **kwargs) -> None:
        self.name: Token = name
        self.args: dict[Any, Any] = kwargs
        self.pos_start: Position = name.pos_start
        self.pos_end: Position = name.pos_end

    def __repr__(self) -> str:
        return f"{self.name} {self.args}"
