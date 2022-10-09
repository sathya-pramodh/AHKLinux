from typing import Any

from base_classes.value import Value


class Function(Value):
    def __init__(self, name: str, parameters: list[Any], body: list[Any]) -> None:
        super().__init__()
        self.name: str = name
        self.parameters: list[Any] = parameters
        self.body: list[Any] = body

    def __repr__(self) -> str:
        return r"{}({}){{}}".format(self.name, self.parameters, self.body)
