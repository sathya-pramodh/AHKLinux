from error_classes.runtime_error import RunTimeError
from base_classes.value import Value
from constants import *


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


class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.boolean = True if self.value else False

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
        return f"'{self.value}'"


class Boolean(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.boolean = True if self.value == "true" else False

    def compare(self, other, operator):
        if operator == "and":
            result = self.boolean and other.boolean
            if result:
                return Boolean("true")
            return Boolean("false")
        elif operator == "or":
            result = self.boolean or other.boolean
            if result:
                return Boolean("true")
            return Boolean("false")

    def copy(self):
        copy = Boolean(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f"{self.value}"


class Array(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.boolean = True if self.value else False

    def set(self, idx, value):
        if str(idx).find(".") != -1:
            return 1, RunTimeError(
                self.pos_start,
                self.pos_end,
                "Expected an integer for an array index.",
                self.context,
            )
        if int(idx) < len(self.value) and int(idx) >= 0:
            self.value[int(idx)] = value
            return 0, None
        return 1, RunTimeError(
            self.pos_start, self.pos_end, "Index out of range.", self.context
        )

    def get(self, idx):
        if str(idx).find(".") != -1:
            return None, RunTimeError(
                self.pos_start,
                self.pos_end,
                "Expected an integer for an array index.",
                self.context,
            )
        if int(idx) < len(self.value) and int(idx) >= 0:
            return self.value[int(idx)], None
        return None, RunTimeError(
            self.pos_start, self.pos_end, "Index out of range.", self.context
        )

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


class AssociativeArray(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.boolean = True if self.value else False

    def set(self, key, value):
        for key_, value_ in self.value.items():
            if key_.value == key:
                self.value[key_] = value
                break
        else:
            if key in DIGITS:
                self.value[Number(key, T_DECIMAL)] = value
            elif key in LETTERS + "_":
                self.value[String(key)] = value

    def get(self, key):
        for key_, value_ in self.value.items():
            if key_.value == key:
                return self.value[key_], None
        return None, RunTimeError(
            self.pos_start,
            self.pos_end,
            "Key '{}' not found in object.".format(key),
            self.context,
        )

    def copy(self):
        copy = Array(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        rep_str = "{"
        count_ = 0
        for key, value in self.value.items():
            if count_ != len(self.value) - 1:
                rep_str += str(key.__repr__()) + ":" + str(value.__repr__()) + ","
            else:
                rep_str += str(key.__repr__()) + ":" + str(value.__repr__())
            count_ += 1
        rep_str += "}"
        return rep_str
