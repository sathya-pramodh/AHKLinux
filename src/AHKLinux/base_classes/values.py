from error_classes.runtime_error import RunTimeError
from constants import *


class Number:
    def __init__(self, value, type_):
        self.value = value
        self.type = type_
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            if self.type == T_HEXADECIMAL and other.type == T_HEXADECIMAL:
                return (
                    Number(
                        hex(int(self.value, base=16) + int(other.value, base=16)),
                        self.type,
                    ).set_context(self.context),
                    None,
                )
            elif self.type == T_HEXADECIMAL and other.type != T_HEXADECIMAL:
                return None, RunTimeError(
                    other.pos_start,
                    other.pos_end,
                    "Invalid Hexadecimal addition",
                    self.context,
                )
            elif self.type != T_HEXADECIMAL and other.type == T_HEXADECIMAL:
                return None, RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    "Invalid Hexadecimal addition",
                    self.context,
                )

            return (
                Number(self.value + other.value, self.type).set_context(self.context),
                None,
            )

    def subtracted_by(self, other):
        if isinstance(other, Number):
            if self.type == T_HEXADECIMAL and other.type == T_HEXADECIMAL:
                return (
                    Number(
                        hex(int(self.value, base=16) - int(other.value, base=16)),
                        self.type,
                    ),
                    None,
                )
            elif self.type == T_HEXADECIMAL and other.type != T_HEXADECIMAL:
                return None, RunTimeError(
                    other.pos_start,
                    other.pos_end,
                    "Invalid Hexadecimal subtraction",
                    self.context,
                )
            elif self.type != T_HEXADECIMAL and other.type == T_HEXADECIMAL:
                return None, RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    "Invalid Hexadecimal subtraction",
                    self.context,
                )
            return (
                Number(self.value - other.value, self.type).set_context(self.context),
                None,
            )

    def multiplied_by(self, other):
        if isinstance(other, Number):
            if self.type == T_HEXADECIMAL and other.type == T_HEXADECIMAL:
                return (
                    Number(
                        hex(int(self.value, base=16) * int(other.value, base=16)),
                        self.type,
                    ),
                    None,
                )
            elif self.type == T_HEXADECIMAL and other.type != T_HEXADECIMAL:
                return None, RunTimeError(
                    other.pos_start,
                    other.pos_end,
                    "Invalid Hexadecimal multiplication",
                    self.context,
                )
            elif self.type != T_HEXADECIMAL and other.type == T_HEXADECIMAL:
                return None, RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    "Invalid Hexadecimal multiplication",
                    self.context,
                )
            return (
                Number(self.value * other.value, self.type).set_context(self.context),
                None,
            )

    def divided_by(self, other):
        if isinstance(other, Number):
            if self.type == T_HEXADECIMAL and other.type == T_HEXADECIMAL:
                if int(other.value, base=16) == 0:
                    return None, RunTimeError(
                        other.pos_start,
                        other.pos_end,
                        "Division by zero not allowed.",
                        self.context,
                    )
                return (
                    Number(
                        hex(int(int(self.value, base=16) / int(other.value, base=16))),
                        self.type,
                    ),
                    None,
                )
            elif self.type == T_HEXADECIMAL and other.type != T_HEXADECIMAL:
                return None, RunTimeError(
                    other.pos_start,
                    other.pos_end,
                    "Invalid Hexadecimal addition",
                    self.context,
                )
            elif self.type != T_HEXADECIMAL and other.type == T_HEXADECIMAL:
                return None, RunTimeError(
                    self.pos_start,
                    self.pos_end,
                    "Invalid Hexadecimal addition",
                    self.context,
                )
            elif other.value == 0:
                return None, RunTimeError(
                    other.pos_start,
                    other.pos_end,
                    "Division by zero not allowed.",
                    self.context,
                )
            return (
                Number(self.value / other.value, self.type).set_context(self.context),
                None,
            )

    def copy(self):
        copy = Number(self.value, self.type)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f"{self.value}"


class String:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def concatenated_to(self, other):
        if not isinstance(other, String):
            return None, RunTimeError(
                self.pos_start,
                self.pos_end,
                "Invalid String concatenation. A string can only be concatenated with another string.",
                self.context,
            )
        return String(self.value + other.value), None

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f"{self.value}"


class Array:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def copy(self):
        copy = Array(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        rep_str = "["
        count_ = 0
        for tok in self.value:
            if count_ != len(self.value) - 1:
                rep_str += str(tok.__repr__()) + ","
            else:
                rep_str += str(tok.__repr__())
            count_ += 1
        rep_str += "]"
        return rep_str
