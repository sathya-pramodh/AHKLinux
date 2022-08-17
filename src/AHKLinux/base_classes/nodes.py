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


class ArrayNode:
    def __init__(self, value_list, pos_start, pos_end):
        self.value_list = value_list
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f"{self.value_list}"


class ObjectNode:
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
        return f"({self.left_node}, {self.op_tok}, {self.right_node})"


class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f"({self.op_tok}, {self.node})"


class VarAssignNode:
    def __init__(self, var_name_tok, value_node, scope="local"):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.scope = scope

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

    def __repr__(self):
        return f"{self.var_name_tok}:{self.value_node}"


class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

    def __repr__(self):
        return f"{self.var_name_tok}"


class ObjectAccessNode:
    def __init__(self, object_name, key):
        self.object_name = object_name
        self.pos_start = self.object_name.pos_start
        self.pos_end = self.object_name.pos_end
        self.key = key

    def __repr__(self):
        return f"{self.object_name}.{self.key}"


class ObjectAssignNode:
    def __init__(self, object_name, key, value):
        self.object_name = object_name
        self.pos_start = self.object_name.pos_start
        self.pos_end = self.object_name.pos_end
        self.key = key
        self.value = value

    def __repr__(self):
        return f"{self.object_name}.{self.key} = {self.value}"
