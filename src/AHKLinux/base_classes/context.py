from typing import Any
from typing_extensions import Self

from base_classes.position import Position
from base_classes.symbol_table import SymbolTable


class Context:
    def __init__(
        self: Self,
        display_name: Any | None,
        parent: Self | None = None,
        parent_entry_pos: Position | None = None,
    ) -> None:
        self.display_name: Any | None = display_name
        self.parent: Self | None = parent
        self.parent_entry_pos: Position | None = parent_entry_pos
        self.symbol_table: SymbolTable = SymbolTable()
