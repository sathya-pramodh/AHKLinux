from base_classes.values import *
from error_classes.runtime_error import RunTimeError
from constants import *
from interpreter.runtime_result import RuntimeResult
from base_classes.nodes import StringNode


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

    def visit_AssociativeArrayNode(self, node, context):
        res = RuntimeResult()
        compiled_arr = {}

        for key_node, value_node in node.value_dict.items():
            compiled_key = res.register(self.visit(key_node, context))
            if res.error:
                return res
            compiled_value = res.register(self.visit(value_node, context))
            if res.error:
                return res
            compiled_arr[compiled_key] = compiled_value
        obj = (
            AssociativeArray(compiled_arr)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )
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
        var_value = var_value.set_context(context).set_pos(node.pos_start, node.pos_end)
        return res.success(var_value)

    def visit_VarAssignNode(self, node, context):
        res = RuntimeResult()
        var_name = node.var_name.value
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

        if node.op_tok.type == T_PLUS:
            right = res.register(self.visit(node.right_node, context))
            if res.error:
                return res
            result, error = left.added_to(right)
            if error:
                return res.failure(error)
            result.set_pos(node.pos_start, node.pos_end)
            return res.success(result)
        elif node.op_tok.type == T_MINUS:
            right = res.register(self.visit(node.right_node, context))
            if res.error:
                return res
            result, error = left.subtracted_by(right)
            if error:
                return res.failure(error)
            result.set_pos(node.pos_start, node.pos_end)
            return res.success(result)

        elif node.op_tok.type == T_MULTIPLY:
            right = res.register(self.visit(node.right_node, context))
            if res.error:
                return res
            result, error = left.multiplied_by(right)
            if error:
                return res.failure(error)
            result.set_pos(node.pos_start, node.pos_end)
            return res.success(result)
        elif node.op_tok.type == T_DIVIDE:
            right = res.register(self.visit(node.right_node, context))
            if res.error:
                return res
            result, error = left.divided_by(right)

            if error:
                return res.failure(error)
            result.set_pos(node.pos_start, node.pos_end)
            return res.success(result)
        elif node.op_tok.type == T_DOT:
            if isinstance(left, String):
                right = res.register(self.visit(node.right_node, context))
                if res.error:
                    return res
                result, error = left.concatenated_to(right)
                if error or result is None:
                    return res.failure(error)
                result.set_pos(node.pos_start, node.pos_end)
                return res.success(result)
            elif isinstance(left, AssociativeArray):
                result, error = left.get(node.right_node.var_name_tok.value)
                if error or result is None:
                    return res.failure(error)
                result.set_pos(node.pos_start, node.pos_end)
                return res.success(result)
            elif isinstance(left, Array):
                if isinstance(node.right_node.var_name_tok.value, int):
                    result, error = left.get(node.right_node.var_name_tok.value)
                    if error or result is None:
                        return res.failure(error)
                    result.set_pos(node.pos_start, node.pos_end)
                    return res.success(result)
                return res.failure(
                    RunTimeError(
                        node.pos_start,
                        node.pos_end,
                        "Expected a Number in '[]'.",
                        context,
                    )
                )
            return res.failure(
                RunTimeError(
                    node.pos_start,
                    node.pos_end,
                    "The object accessed is not a string, an Array or an Associative Array.",
                    context,
                )
            )

    def visit_AssociativeArrayAssignNode(self, node, context):
        res = RuntimeResult()
        compiled_access_node = res.register(self.visit(node.access_node, context))
        if res.error:
            return res
        compiled_value = res.register(self.visit(node.value_node, context))
        if res.error:
            return res
        if isinstance(compiled_access_node, AssociativeArray):
            compiled_access_node.set(node.key.var_name_tok.value, compiled_value)
            return res.success(
                "Key '{}' was assigned the value {}.".format(
                    node.key.var_name_tok.value, compiled_value
                )
            )
        if isinstance(compiled_access_node, Array):
            ret_code, error = compiled_access_node.set(node.key.value, compiled_value)
            if error:
                return res.failure(error)
            return res.success(
                "Index {} was assigned the value {}.".format(
                    node.key.var_name_tok.value, compiled_value
                )
            )
        return res.failure(
            RunTimeError(
                node.pos_start,
                node.pos_end,
                "{} is not an Array or an Associative Array.".format(node.access_node),
                context,
            )
        )

    def visit_AssociativeArrayAccessNode(self, node, context):
        res = RuntimeResult()
        compiled_access_node = res.register(self.visit(node.access_node, context))
        if res.error:
            return res

        if isinstance(compiled_access_node, AssociativeArray):
            value, error = compiled_access_node.get(node.key.var_name_tok.value)
            if error:
                return res.failure(error)
            return res.success(value)

        if isinstance(compiled_access_node, String):
            right = res.register(self.visit(node.key, context))
            if res.error:
                return res
            result, error = compiled_access_node.concatenated_to(right)
            if error:
                return res.failure(error)
            return res.success(result)

        if isinstance(compiled_access_node, Array):
            if isinstance(node.key.var_name_tok.value, int):
                value, error = compiled_access_node.get(node.key.var_name_tok.value)
                if error or value is None:
                    return res.failure(error)
                value.set_pos(node.pos_start, node.pos_end)
                return res.success(value)
            return res.failure(
                RunTimeError(
                    node.pos_start,
                    node.pos_end,
                    "Expected a number inside '[]'.",
                    context,
                )
            )

        return res.failure(
            RunTimeError(
                node.pos_start,
                node.pos_end,
                "The object accessed is not a String, an Array or an Associative Array.",
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
