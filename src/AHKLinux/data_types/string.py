from base_classes.value import Value
from constants import ESCAPE_CHARS
from error_classes.runtime_error import RunTimeError


class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = self.replace_escape_chars(value)
        self.boolean = True if self.value else False

    def replace_escape_chars(self, value):
        for key_, value_ in ESCAPE_CHARS.items():
            value = value.replace(key_, value_)
        return value

    def concatenated_to(self, other):
        if not isinstance(other, String) or self.value is None or other.value is None:
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
