from typing import Any, Self


class Position:
    def __init__(self, filename: str, idx: int, line: int, ftext: str) -> None:
        self.filename: str = filename
        self.idx: int = idx
        self.line: int = line
        self.ftext: str = ftext

    def advance(self, current_char: Any) -> Self:
        self.idx += 1
        if current_char == "\n":
            self.line += 1
        return self

    def copy(self) -> Self:
        return Position(self.filename, self.idx, self.line, self.ftext)
