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

    def __repr__(self):
        return f"{self.value}"
