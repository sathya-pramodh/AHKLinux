from constants import T_DOT
from base_classes.tokens import Token


class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f"{self.tok}"


class StringNode:
    def __init__(self, tok, quoted=True):
        self.tok = tok
        self.quoted = quoted
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f"{self.tok}"


class BooleanNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f"{self.tok}"


class ArrayNode:
    def __init__(self, value_list, pos_start, pos_end):
        self.value_list = value_list
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"{self.value_list}"


class AssociativeArrayNode:
    def __init__(self, value_dict, pos_start, pos_end):
        self.value_dict = value_dict
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"{self.value_dict}"


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        if self.op_tok.type == T_DOT:
            return f"{self.left_node}.{self.right_node}"
        return f"{self.left_node} {self.op_tok} {self.right_node}"


class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f"({self.op_tok}, {self.node})"


class TernaryOpNode:
    def __init__(self, condition_node, true_node, false_node):
        self.condition_node = condition_node
        self.true_node = true_node
        self.false_node = false_node
        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.false_node.pos_end

    def __repr__(self):
        return f"{self.condition_node} ? {self.true_node}:{self.false_node}"


class VarAssignNode:
    def __init__(self, var_name, value_node, scope="local"):
        self.var_name = var_name
        self.value_node = value_node
        self.scope = scope

        self.pos_start = self.var_name.pos_start
        self.pos_end = self.value_node.pos_end

    def __repr__(self):
        return f"{self.var_name}:{self.value_node}"


class L_VarAssignNode:
    def __init__(self, var_name, string_node, var_nodes):
        self.var_name = var_name
        self.string_node = string_node
        self.var_nodes = var_nodes
        self.pos_start = self.var_name.pos_start
        self.pos_end = self.var_name.pos_end

    def __repr__(self):
        return f"{self.var_name}:{self.string_node}"


class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

    def __repr__(self):
        return f"{self.var_name_tok}"


class ObjectAssignNode:
    def __init__(self, access_node, key, access_method, value_node):
        self.access_node = access_node
        self.key = key
        self.access_method = access_method
        self.value_node = value_node
        self.pos_start = self.access_node.pos_start
        self.pos_end = self.access_node.pos_end

    def __repr__(self):
        return f"{self.access_node}.{self.key}:{self.value_node}"


class ObjectAccessNode:
    def __init__(self, access_node, key, access_method):
        self.access_node = access_node
        self.key = key
        self.access_method = access_method
        self.pos_start = self.access_node.pos_start
        self.pos_end = self.access_node.pos_end

    def __repr__(self):
        return f"{self.access_node} {self.access_method} {self.key}"


class ObjectKeyNode:
    def __init__(self, node):
        self.node = node
        if isinstance(self.node, Token):
            self.name = self.node.value
        elif isinstance(self.node, UnaryOpNode) or isinstance(self.node, BinOpNode):
            self.name = None
        else:
            self.name = self.node.tok.value
        self.pos_start = self.node.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f"{self.node}"


class IfNode:
    def __init__(self, condition_node, if_body):
        self.condition_node = condition_node
        self.if_body = if_body
        self.pos_start = self.condition_node.pos_start
        self.pos_end = (
            self.if_body[-1].pos_end
            if self.if_body != []
            else self.condition_node.pos_end
        )

    def __repr__(self):
        return f"if {self.condition_node} then {self.if_body}"


class IfElseNode:
    def __init__(self, condition_node, if_body, else_body):
        self.condition_node = condition_node
        self.if_body = if_body
        self.else_body = else_body
        self.pos_start = self.condition_node.pos_start
        if self.else_body != []:
            self.pos_end = self.else_body[-1].pos_end
        elif self.if_body != []:
            self.pos_end = self.if_body[-1].pos_end
        else:
            self.pos_end = self.condition_node.pos_end

    def __repr__(self):
        return f"if {self.condition_node} then {self.if_body} else {self.else_body}"


class FunctionDeclareNode:
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.pos_start = name.pos_start
        self.pos_end = (
            self.body[-1].pos_end
            if self.body[-1] is not None
            else self.body[-2].pos_end
        )

    def __repr__(self):
        return r"{}({}){{}}".format(self.name, self.parameters, self.body)


class FunctionCallNode:
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters
        self.pos_start = name.pos_start
        self.pos_end = (
            self.parameters[-1].pos_end if self.parameters != [] else name.pos_end
        )

    def __repr__(self):
        return r"{}({})".format(self.name, self.parameters)


class ReturnNode:
    def __init__(self, node):
        self.node = node
        self.pos_start = self.node.pos_start if self.node is not None else None
        self.pos_end = self.node.pos_end if self.node is not None else None

    def __repr__(self):
        return f"return {self.node}"


class CommandNode:
    def __init__(self, name, **kwargs):
        self.name = name
        self.args = kwargs
        self.pos_start = name.pos_start
        self.pos_end = name.pos_end

    def __repr__(self):
        return f"{self.name} {self.args}"
