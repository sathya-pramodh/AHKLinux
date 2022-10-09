from typing import Any, Self

from base_classes.error import Error


class ParseResult:
    def __init__(self) -> None:
        self.error: Error | None = None
        self.node: Any | None = None
        self.advance_count: int = 0

    def __repr__(self) -> str:
        return f"{self.node}"

    def register_advancement(self) -> None:
        self.advance_count += 1

    def register_recession(self) -> None:
        if self.advance_count - 1 >= 0:
            self.advance_count -= 1

    def register(self, res: Any) -> Any | None:
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def success(self, node: Any) -> Self:
        self.node = node
        return self

    def failure(self, error: Error) -> Self:
        if not self.error or self.advance_count == 0:
            self.error = error
        return self
