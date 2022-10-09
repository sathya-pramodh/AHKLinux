from typing import Self

from base_classes.context import Context
from base_classes.position import Position


class Value:
    def __init__(self) -> None:
        self.set_pos()
        self.set_context()

    def set_pos(
        self, pos_start: Position | None = None, pos_end: Position | None = None
    ) -> Self:
        self.pos_start: Position | None = pos_start
        self.pos_end: Position | None = pos_end
        return self

    def set_context(self, context: Context | None = None) -> Self:
        self.context: Context | None = context
        return self
