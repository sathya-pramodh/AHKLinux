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
        return RuntimeResult().success(
            Number(node.tok.value, node.tok.type)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )

    def visit_StringNode(self, node, context):
        return RuntimeResult().success(
            String(node.tok.value)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )

    def visit_ArrayNode(self, node, context):
        res = RuntimeResult()
        elements = []

        for element_node in node.value_list:
            elements.append(res.register(self.visit(element_node, context)))
            if res.error:
                return res
        return res.success(
            Array(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ObjectNode(self, node, context):
        res = RuntimeResult()
        elements = {}

        for key, value in node.value_dict.items():
            compiled_key = res.register(self.visit(key, context))
            if res.error:
                return res
            compiled_value = res.register(self.visit(value, context))
            if res.error:
                return res
            elements[compiled_key] = compiled_value
        return res.success(
            Object(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

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
        return res.success(var_value)

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
            return res.success(result.set_pos(node.pos_start, node.pos_end))
        elif node.op_tok.type == T_MINUS:
            result, error = left.subtracted_by(right)
            if error:
                return res.failure(error)
            return res.success(result.set_pos(node.pos_start, node.pos_end))
        elif node.op_tok.type == T_MULTIPLY:
            result, error = left.multiplied_by(right)
            if error:
                return res.failure(error)
            return res.success(result.set_pos(node.pos_start, node.pos_end))
        elif node.op_tok.type == T_DIVIDE:
            result, error = left.divided_by(right)

            if error:
                return res.failure(error)
            return res.success(result.set_pos(node.pos_start, node.pos_end))
        elif node.op_tok.type == T_DOT:
            if isinstance(left, String) and isinstance(right, String):
                result, error = left.concatenated_to(right)
                if error:
                    return res.failure(error)
                return res.success(result.set_pos(node.pos_start, node.pos_end))
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
        return res.success(number.set_pos(node.pos_start, node.pos_end))
