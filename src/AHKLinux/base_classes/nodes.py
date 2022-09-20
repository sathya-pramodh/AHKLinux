from constants import T_DOT


class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f"{self.tok}"


class StringNode:
    def __init__(self, tok):
        self.tok = tok
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
        return f"{self.left_node} {self.op_tok.type} {self.right_node}"


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
        return f"{self.access_node}.{self.key}"


class IfNode:
    def __init__(self, condition_node, statements):
        self.condition_node = condition_node
        self.statements = statements
        self.pos_start = self.condition_node.pos_start
        self.pos_end = (
            self.statements[-1].pos_end
            if self.statements != []
            else self.condition_node.pos_end
        )

    def __repr__(self):
        return f"if {self.condition_node} then {self.statements}"


class IfElseNode:
    def __init__(self, condition_node, statements, else_statements):
        self.condition_node = condition_node
        self.statements = statements
        self.else_statements = else_statements
        self.pos_start = self.condition_node.pos_start
        if self.else_statements != []:
            self.pos_end = self.else_statements[-1].pos_end
        elif self.statements != []:
            self.pos_end = self.statements[-1].pos_end
        else:
            self.pos_end = self.condition_node.pos_end

    def __repr__(self):
        return f"if {self.condition_node} then {self.statements} else {self.else_statements}"


class FunctionDeclareNode:
    def __init__(self, name, parameters, statements):
        self.name = name
        self.parameters = parameters
        self.statements = statements
        self.pos_start = name.pos_start
        self.pos_end = self.statements[-1].pos_end

    def __repr__(self):
        return r"{}({}){{}}".format(self.name, self.parameters, self.statements)


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
