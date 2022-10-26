from typing import Any
from typing_extensions import Self

from base_classes.value import Value
from constants import DIGITS, LETTERS, T_DECIMAL
from data_types.boolean import Boolean
from data_types.number import Number
from data_types.string import String
from error_classes.runtime_error import RunTimeError


class AssociativeArray(Value):
    def __init__(self, value: dict[Any, Any]) -> None:
        super().__init__()
        self.value: dict[Any, Any] = value
        self.boolean: bool = True if self.value else False
        self.repr_boolean: Boolean = Boolean("true") if self.value else Boolean("false")

    def set(self, key: str, value: Any) -> None:
        for key_ in self.value:
            if key_.value == key:
                self.value[key_] = value
                break
        else:
            if key in DIGITS:
                self.value[Number(key, T_DECIMAL)] = value
            elif key in LETTERS + "_":
                self.value[String(key)] = value

    def get(self, key) -> tuple[Any | None, RunTimeError | None]:
        for key_ in self.value:
            if key_.value == key:
                return self.value[key_], None
        return None, RunTimeError(
            self.pos_start,
            self.pos_end,
            "Key '{}' not found in object.".format(key),
            self.context,
        )

    def copy(self) -> Self:
        copy: AssociativeArray = AssociativeArray(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self) -> str:
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
