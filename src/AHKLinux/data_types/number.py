from base_classes.value import Value
from constants import T_HEXADECIMAL
from error_classes.runtime_error import RunTimeError


class Number(Value):
    def __init__(self, value, type_):
        super().__init__()
        self.value = value
        self.type = type_
        if self.type == T_HEXADECIMAL:
            self.boolean = True if int(self.value, base=16) != 0 else False
        else:
            self.boolean = True if self.value else False

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