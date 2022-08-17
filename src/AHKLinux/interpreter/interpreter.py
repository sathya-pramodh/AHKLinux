from base_classes.values import *
from error_classes.runtime_error import RunTimeError
from constants import *
from interpreter.runtime_result import RuntimeResult


class Interpreter:
    def visit(self, node, context):
        method_name = "visit_{}".format(type(node).__name__)
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception("No visit_{} method defined.".format(type(node).__name__))

    def visit_NumberNode(self, node, context):
        number = (
            Number(node.tok.value, node.tok.type)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )
        return RuntimeResult().success(number)

    def visit_StringNode(self, node, context):
        string = (
            String(node.tok.value)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )
        return RuntimeResult().success(string)

    def visit_ArrayNode(self, node, context):
        res = RuntimeResult()
        elements = []

        for element_node in node.value_list:
            elements.append(res.register(self.visit(element_node, context)))
            if res.error:
                return res
        arr = Array(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        return res.success(arr)

    def visit_ObjectNode(self, node, context):
        obj = Object({}).set_context(context).set_pos(node.pos_start, node.pos_end)
        return RuntimeResult().success(obj)

    def visit_VarAccessNode(self, node, context):
        res = RuntimeResult()
        var_name = node.var_name_tok.value
        var_value = None
        for name, value in context.symbol_table.symbols.items():
            if name.lower() == var_name.lower():
                var_value = value

        if not var_value:
            return res.failure(
                RunTimeError(
                    node.pos_start,
                    node.pos_end,
                    "'{}' is not defined.".format(var_name),
                    context,
                )
            )
        var_value = var_value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(var_value)

    def visit_VarAssignNode(self, node, context):
        res = RuntimeResult()
        var_name = node.var_name_tok.value
        var_value = res.register(self.visit(node.value_node, context))
        if res.error:
            return res
        for name in context.symbol_table.symbols.keys():
            if name.lower() == var_name.lower():
                context.symbol_table.symbols[name] = var_value
                break
        if node.scope == "global":
            context.symbol_table.set(var_name, var_value, global_=True)
        else:
            context.symbol_table.set(var_name, var_value)
        return res.success(
            "'{}' has been assigned the value {}.".format(var_name, var_value)
        )

    def visit_BinOpNode(self, node, context):
        res = RuntimeResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        right = res.register(self.visit(node.right_node, context))
        if res.error:
            return res

        if node.op_tok.type == T_PLUS:
            result, error = left.added_to(right)
            if error:
                return res.failure(error)
            result.set_pos(node.pos_start, node.pos_end)
            return res.success(result)
        elif node.op_tok.type == T_MINUS:
            result, error = left.subtracted_by(right)
            if error:
                return res.failure(error)
            result.set_pos(node.pos_start, node.pos_end)
            return res.success(result)
        elif node.op_tok.type == T_MULTIPLY:
            result, error = left.multiplied_by(right)
            if error:
                return res.failure(error)
            result.set_pos(node.pos_start, node.pos_end)
            return res.success(result)
        elif node.op_tok.type == T_DIVIDE:
            result, error = left.divided_by(right)

            if error:
                return res.failure(error)
            result.set_pos(node.pos_start, node.pos_end)
            return res.success(result)
        elif node.op_tok.type == T_DOT:
            if isinstance(left, String) and isinstance(right, String):
                result, error = left.concatenated_to(right)
                if error or result is None:
                    return res.failure(error)
                result.set_pos(node.pos_start, node.pos_end)
                return res.success(result)
            return res.failure(
                RunTimeError(
                    node.pos_start,
                    node.pos_end,
                    "Invalid String concatenation. A string can only be concatenated with another string.",
                    context,
                )
            )

    def visit_UnaryOpNode(self, node, context):
        res = RuntimeResult()
        number = res.register(self.visit(node.node, context))
        if res.error:
            return res

        if node.op_tok.type == T_MINUS:
            if number.type == T_HEXADECIMAL:
                number, error = number.multiplied_by(Number("-0x1", T_HEXADECIMAL))
                if error:
                    return res.failure(error)
            else:
                number, error = number.multiplied_by(Number(-1, T_DECIMAL))
                if error:
                    return res.failure(error)
        number.set_pos(node.pos_start, node.pos_end)
        return res.success(number)

    def visit_ObjectAccessNode(self, node, context):
        res = RuntimeResult()
        object_name = self.visit(node.object_name, context)
        if object_name.error:
            return res.failure(object_name.error)
        result = object_name.value.get(node.key.value)
        if result is None:
            return res.failure(
                RunTimeError(
                    node.pos_start,
                    node.pos_end,
                    "Key '{}' not found in object.".format(node.key.value),
                    context,
                )
            )
        return res.success(result)

    def visit_ObjectAssignNode(self, node, context):
        res = RuntimeResult()
        object_name = self.visit(node.object_name, context)
        value = self.visit(node.value, context)
        if value.error:
            return res.failure(value.error)
        object_name.value.set(str(node.key.value), value.value)
        object_name.value.set_pos(node.pos_start, node.pos_end)
        return res.success(
            "Key '{}' in object {} has been assigned the value {}.".format(
                node.key, object_name.value, value.value
            )
        )
