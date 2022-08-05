from base_classes.values import Number
from error_classes.runtime_error import RunTimeError
from constants import *
from interpreter.runtime_result import RuntimeResult
import sys


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

    def visit_VarAccessNode(self, node, context):
        res = RuntimeResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)
        if not value:
            return res.failure(
                RunTimeError(
                    node.pos_start,
                    node.pos_end,
                    "'{}' is not defined.".format(var_name),
                    context,
                )
            )
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RuntimeResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error:
            return res
        if node.scope == "global":
            context.symbol_table.set(var_name, value, global_=True)
        else:
            context.symbol_table.set(var_name, value)
        return res.success(value)

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
