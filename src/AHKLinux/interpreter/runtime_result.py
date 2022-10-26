from typing import Any
from typing_extensions import Self

from base_classes.error import Error


class RuntimeResult:
    def __init__(self) -> None:
        self.value: Any | None = None
        self.error: Any | None = None

    def register(self, res: Any) -> Any:
        if res.error:
            self.error = res.error
        return res.value

    def success(self, value: Any) -> Self:
        self.value = value
        return self

    def failure(self, error: Any) -> Self:
        self.error = error
        return self

    def __repr__(self) -> str:
        if not self.error:
            return f"{self.value}"
        return f"{self.error}"
