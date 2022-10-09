from typing import Any

from base_classes.position import Position


class Token:
    def __init__(
        self,
        type_: str,
        value: Any = None,
        pos_start: Position | None = None,
        pos_end: Position | None = None,
    ) -> None:
        self.type: str = type_
        self.value: Any | None = value
        if pos_start:
            self.pos_start: Position = pos_start.copy()
            self.pos_end: Position = pos_start.copy()

        if pos_end:
            self.pos_end: Position = pos_end

    def matches(self, type_: str, value: Any | None) -> bool:
        return self.type == type_ and self.value == value

    def __repr__(self) -> str:
        if self.value == 0 or self.value:
            return f"{self.value}"
        return f"{self.type}"
