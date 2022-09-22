import re

from base_classes.context import Context
from base_classes.nodes import ReturnNode, StringNode, VarAccessNode
from base_classes.symbol_table import SymbolTable
from constants import *
from data_types.array import Array
from data_types.associative_array import AssociativeArray
from data_types.boolean import Boolean
from data_types.function import Function
from data_types.number import Number
from data_types.string import String
from error_classes.runtime_error import RunTimeError
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
        if not node.quoted:
            var_names = re.findall("%[a-zA-Z0-9_@#$]*%", node.tok.value)
            for var_name in var_names:
                var_name = var_name.replace("%", "")
                var_value = context.symbol_table.get(var_name)
                if var_value is None:
                    return RuntimeResult().failure(
                        RunTimeError(
                            node.pos_start,
                            node.pos_end,
                            "'{}' is not defined.".format(var_name),
                            context,
                        )
                    )
                if not (isinstance(var_value, String) or isinstance(var_value, Number)):
                    return RuntimeResult().failure(
                        RunTimeError(
                            node.pos_start,
                            node.pos_end,
                            "'{}' is not a string or a number.".format(var_name),
                            context,
                        )
                    )
                node.tok.value = re.sub(
                    "%[a-zA-Z0-9_@#$]*%",
                    str(var_value),
                    node.tok.value,
                    count=1,
                )

        string = (
            String(node.tok.value)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )
        return RuntimeResult().success(string)

    def visit_BooleanNode(self, node, context):
        boolean = (
            Boolean(node.tok.value)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )
        return RuntimeResult().success(boolean)

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
        return res.success(obj)

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
        var_value.set_context(context).set_pos(node.pos_start, node.pos_end)
        return res.success(
            "'{}' has been assigned the value {}.".format(var_name, var_value)
        )

    def visit_L_VarAssignNode(self, node, context):
        res = RuntimeResult()
        var_name = node.var_name.value
        var_values = []
        for var_node in node.var_nodes:
            var_value = res.register(self.visit(var_node, context))
            if res.error:
                return res
            var_values.append(var_value)
        node.string_node.tok.value.format(*var_values)
        value = res.register(self.visit(node.string_node, context))
        if res.error:
            return res
        context.symbol_table.set(var_name, value)
        return res.success(
            "'{}' has been assigned the value {}.".format(var_name, value)
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
            result.set_context(context).set_pos(node.pos_start, node.pos_end)
            return res.success(result)
        elif node.op_tok.type == T_MINUS:
            right = res.register(self.visit(node.right_node, context))
            if res.error:
                return res
            result, error = left.subtracted_by(right)
            if error:
                return res.failure(error)
            result.set_context(context).set_pos(node.pos_start, node.pos_end)
            return res.success(result)

        elif node.op_tok.type == T_MULTIPLY:
            right = res.register(self.visit(node.right_node, context))
            if res.error:
                return res
            result, error = left.multiplied_by(right)
            if error:
                return res.failure(error)
            result.set_context(context).set_pos(node.pos_start, node.pos_end)
            return res.success(result)
        elif node.op_tok.type == T_DIVIDE:
            right = res.register(self.visit(node.right_node, context))
            if res.error:
                return res
            result, error = left.divided_by(right)

            if error:
                return res.failure(error)
            result.set_context(context).set_pos(node.pos_start, node.pos_end)
            return res.success(result)
        elif node.op_tok.type == T_DOT:
            if isinstance(left, String):
                right = res.register(self.visit(node.right_node, context))
                if res.error:
                    return res
                result, error = left.concatenated_to(right)
                if error or result is None:
                    return res.failure(error)
                result.set_context(context).set_pos(node.pos_start, node.pos_end)
                return res.success(result)
            elif isinstance(left, AssociativeArray):
                if isinstance(node.right_node, StringNode):
                    return res.failure(
                        RunTimeError(
                            node.pos_start,
                            node.pos_end,
                            "{} is not a String.".format(left),
                            context,
                        )
                    )
                result, error = left.get(node.right_node.var_name_tok.value)
                if error or result is None:
                    return res.failure(error)
                result.set_context(context).set_pos(node.pos_start, node.pos_end)
                return res.success(result)
            return res.failure(
                RunTimeError(
                    node.pos_start,
                    node.pos_end,
                    "The object accessed is not a string or an Associative Array.",
                    context,
                )
            )
        elif node.op_tok.type == T_LSQUARE:
            if isinstance(left, Array):
                if isinstance(node.right_node.var_name_tok.value, int):
                    result, error = left.get(node.right_node.var_name_tok.value)
                    if error or result is None:
                        return res.failure(error)
                    result.set_context(context).set_pos(node.pos_start, node.pos_end)
                    return res.success(result)
                return res.failure(
                    RunTimeError(
                        node.pos_start,
                        node.pos_end,
                        "Expected a Number in '[]'.",
                        context,
                    )
                )
            elif isinstance(left, String):
                right = res.register(self.visit(node.right_node, context))
                if res.error:
                    return res
                result, error = left.concatenated_to(right)
                if error or result is None:
                    return res.failure(error)
                result.set_context(context).set_pos(node.pos_start, node.pos_end)
                return res.success(result)
            elif isinstance(left, AssociativeArray):
                if node.right_node.var_name_tok.type == T_IDENTIFIER:
                    right = res.register(self.visit(node.right_node, context))
                    if res.error:
                        return res
                    result, error = left.get(right.value)
                    if error or result is None:
                        return res.failure(error)
                    result.set_context(context).set_pos(node.pos_start, node.pos_end)
                    return res.success(result)
                result, error = left.get(node.right_node.var_name_tok.value)
                if error or result is None:
                    return res.failure(error)
                result.set_context(context).set_pos(node.pos_start, node.pos_end)
                return res.success(result)

            return res.failure(
                RunTimeError(
                    node.pos_start,
                    node.pos_end,
                    "The object accessed is not a string, an Array or an Associative Array.",
                    context,
                )
            )

        elif node.op_tok.matches(T_KEYWORD, "and") or node.op_tok.matches(
            T_KEYWORD, "or"
        ):
            right = res.register(self.visit(node.right_node, context))
            if res.error:
                return res
            operator = "and" if node.op_tok.matches(T_KEYWORD, "and") else "or"
            result = left.compare(right, operator)
            result.set_context(context).set_pos(node.pos_start, node.pos_end)
            return res.success(result)

    def visit_UnaryOpNode(self, node, context):
        res = RuntimeResult()
        number = res.register(self.visit(node.node, context))
        if res.error:
            return res

        if node.op_tok.matches(T_KEYWORD, "not"):
            if number.boolean:
                boolean = (
                    Boolean("false")
                    .set_context(context)
                    .set_pos(node.pos_start, node.pos_end)
                )
                return res.success(boolean)
            boolean = (
                Boolean("true")
                .set_context(context)
                .set_pos(node.pos_start, node.pos_end)
            )
            return res.success(boolean)

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

    def visit_TernaryOpNode(self, node, context):
        res = RuntimeResult()
        condition = res.register(self.visit(node.condition_node, context))
        if res.error:
            return res
        if condition.boolean:
            compiled_true_node = res.register(self.visit(node.true_node, context))
            if res.error:
                return res
            return res.success(compiled_true_node)
        else:
            compiled_false_node = res.register(self.visit(node.false_node, context))
            if res.error:
                return res
            return res.success(compiled_false_node)

    def visit_ObjectAssignNode(self, node, context):
        res = RuntimeResult()
        compiled_access_node = res.register(self.visit(node.access_node, context))
        if res.error:
            return res
        compiled_value = res.register(self.visit(node.value_node, context))
        if res.error:
            return res
        if isinstance(compiled_access_node, AssociativeArray):
            if node.access_method == T_LSQUARE:
                if node.key.var_name_tok.type == T_IDENTIFIER:
                    right = res.register(self.visit(node.key, context))
                    if res.error:
                        return res
                    compiled_access_node.set(right.value, compiled_value)
                    compiled_value.set_context(context).set_pos(
                        node.pos_start, node.pos_end
                    )
                    return res.success(
                        "Key '{}' was assigned the value {}.".format(
                            node.key.var_name_tok.value, compiled_value
                        )
                    )
            compiled_access_node.set(node.key.var_name_tok.value, compiled_value)
            compiled_value.set_context(context).set_pos(node.pos_start, node.pos_end)
            return res.success(
                "Key '{}' was assigned the value {}.".format(
                    node.key.var_name_tok.value, compiled_value
                )
            )
        if isinstance(compiled_access_node, Array):
            if isinstance(node.key.var_name_tok.value, int):
                ret_code, error = compiled_access_node.set(
                    node.key.var_name_tok.value, compiled_value
                )
                if error:
                    return res.failure(error)
                compiled_value.set_context(context).set_pos(
                    node.pos_start, node.pos_end
                )
                return res.success(
                    "Index {} was assigned the value {}.".format(
                        node.key.var_name_tok.value, compiled_value
                    )
                )
            return res.failure(
                RunTimeError(
                    node.pos_start,
                    node.pos_end,
                    "Array indices can only be integers.",
                    context,
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

    def visit_ObjectAccessNode(self, node, context):
        res = RuntimeResult()
        compiled_access_node = res.register(self.visit(node.access_node, context))
        if res.error:
            return res

        if isinstance(compiled_access_node, AssociativeArray):
            if node.access_method == T_LSQUARE:
                if node.key.var_name_tok.type == T_IDENTIFIER:
                    right = res.register(self.visit(node.key, context))
                    if res.error:
                        return res
                    value, error = compiled_access_node.get(right.value)
                    if error or value is None:
                        return res.failure(error)
                    value.set_context(context).set_pos(node.pos_start, node.pos_end)
                    return res.success(value)
            if isinstance(node.key, StringNode):
                return res.failure(
                    RunTimeError(
                        node.pos_start,
                        node.pos_end,
                        "{} is not a String.".format(compiled_access_node),
                        context,
                    )
                )
            value, error = compiled_access_node.get(node.key.var_name_tok.value)
            if error or value is None:
                return res.failure(error)
            value.set_context(context).set_pos(node.pos_start, node.pos_end)
            return res.success(value)

        if isinstance(compiled_access_node, String):
            right = res.register(self.visit(node.key, context))
            if res.error:
                return res
            result, error = compiled_access_node.concatenated_to(right)
            if error or result is None:
                return res.failure(error)
            result.set_pos(node.pos_start, node.pos_end)
            return res.success(result)

        if isinstance(compiled_access_node, Array):
            if isinstance(node.key.var_name_tok.value, int):
                if node.access_method == T_DOT:
                    return res.failure(
                        RunTimeError(
                            node.pos_start,
                            node.pos_end,
                            "Cannot use '.' for this operation.",
                            context,
                        )
                    )
                value, error = compiled_access_node.get(node.key.var_name_tok.value)
                if error or value is None:
                    return res.failure(error)
                value.set_pos(node.pos_start, node.pos_end)
                return res.success(value)
            return res.failure(
                RunTimeError(
                    node.pos_start,
                    node.pos_end,
                    "Array indices can only be integers.",
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

    def visit_IfNode(self, node, context):
        res = RuntimeResult()
        condition = res.register(self.visit(node.condition_node, context))
        if res.error:
            return res
        if condition.boolean:
            outputs = []
            for expr in node.statements:
                result = res.register(self.visit(expr, context))
                if res.error:
                    return res
                outputs.append(result)
            return res.success(outputs)
        return res.success([])

    def visit_IfElseNode(self, node, context):
        res = RuntimeResult()
        condition = res.register(self.visit(node.condition_node, context))
        if res.error:
            return res
        if condition.boolean:
            outputs = []
            for expr in node.statements:
                result = res.register(self.visit(expr, context))
                if res.error:
                    return res
                outputs.append(result)
            return res.success(outputs)
        outputs = []
        for expr in node.else_statements:
            result = res.register(self.visit(expr, context))
            if res.error:
                return res
            outputs.append(result)
        return res.success(outputs)

    def visit_FunctionDeclareNode(self, node, context):
        res = RuntimeResult()
        for parameter in node.parameters:
            if not isinstance(parameter, VarAccessNode):
                return res.failure(
                    RunTimeError(
                        node.pos_start,
                        node.pos_end,
                        "Expected identifiers as parameters inside function declaration.",
                        context,
                    )
                )
        result = (
            Function(node.name.value, node.parameters, node.statements)
            .set_pos(node.pos_start, node.pos_end)
            .set_context(context)
        )
        context.symbol_table.set(node.name.value, result)
        return res.success(
            "Function with name '{}' has been declared.".format(node.name.value)
        )

    def visit_FunctionCallNode(self, node, context):
        res = RuntimeResult()
        func = context.symbol_table.get(node.name.value)
        if len(node.parameters) != len(func.parameters):
            return res.failure(
                RunTimeError(
                    node.pos_start,
                    node.pos_end,
                    "Parameter mismatch. Function call misses one or more required parameters.",
                    context,
                )
            )
        function_context = Context(node.name.value)
        function_context.parent = context
        function_context.parent_entry_pos = node.pos_start
        function_context.symbol_table = SymbolTable({})
        function_context.symbol_table.parent = context.symbol_table
        idx = 0
        for parameter in func.parameters:
            param_value = res.register(self.visit(node.parameters[idx], context))
            if res.error:
                return res
            param_value.set_pos(node.pos_start, node.pos_end).set_context(
                function_context
            )
            function_context.symbol_table.set(parameter.var_name_tok.value, param_value)
            idx += 1

        for statement in func.statements:
            if isinstance(statement, ReturnNode):
                result = res.register(self.visit(statement, function_context))
                if res.error:
                    return res
                return res.success(result)
            res.register(self.visit(statement, function_context))
            if res.error:
                return res
        return res.success(String(""))

    def visit_ReturnNode(self, node, context):
        res = RuntimeResult()
        if context.display_name == "<module>":
            if node.node is None:
                return res.success(String(""))
            return res.failure(
                RunTimeError(
                    node.pos_start,
                    node.pos_end,
                    "Return statement cannot be used here.",
                    context,
                )
            )
        if node.node is None:
            value = String("")
        else:
            value = res.register(self.visit(node.node, context))
        if res.error:
            return res
        return res.success(value)
