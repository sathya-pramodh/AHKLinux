from typing import Any


class SymbolTable:
    def __init__(self, symbols: dict[str, Any] = {}) -> None:
        self.symbols: dict[str, Any] = symbols
        self.parent: SymbolTable | None = None

    def get(self, name: str) -> Any:
        for name_ in self.symbols:
            if name_.lower() == name.lower():
                return self.symbols[name_][0]

    def set(self, name: str, value: tuple[Any, bool]) -> None:
        for name_ in self.symbols:
            if name_.lower() == name.lower():
                self.symbols[name_] = value
                break
        else:
            self.symbols[name] = value

    def remove(self, name: str) -> None:
        del self.symbols[name]

    def global_from_child(self, name: str) -> Any | bool:
        for name_ in self.symbols.keys():
            if name_.lower() == name.lower():
                return self.symbols[name_][1]
        return False
