from typing import Self

from base_classes.value import Value


class Boolean(Value):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value: str = value
        self.boolean: bool = True if self.value == "true" else False
        self.repr_boolean: Self = self

    def compare(self, other: Self, operator: str) -> Self:
        if operator == "and":
            result = self.boolean and other.boolean
            if result:
                return Boolean("true")
            return Boolean("false")
        else:
            result = self.boolean or other.boolean
            if result:
                return Boolean("true")
            return Boolean("false")

    def copy(self) -> Self:
        copy: Self = Boolean(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self) -> str:
        return f"{self.value}"
