from base_classes.value import Value
from error_classes.runtime_error import RunTimeError


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
