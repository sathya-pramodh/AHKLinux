class Global:
    pass


class Boolean:
    pass


class Equals:
    pass


class String:
    pass


class Floating:
    pass


class Decimal:
    pass


class Hexadecimal:
    pass


class Variable:
    pass


class SingleComment:
    pass


class Token:
    """
    A Token base class to represent all the tokens in the AutoHotKey script.
    """

    def __init__(self, identifier, name):
        self._identifier = identifier
        self._name = name
        self.__super__ = self._classify()

    def _classify(self):
        if self._identifier == "GLOBAL":
            return Global()
        if self._identifier == "BOOLEAN":
            return Boolean()
        if self._identifier == "EQUALS":
            return Boolean()
        if self._identifier == "STRING":
            return String()
        if self._identifier == "FLOATING":
            return Floating()
        if self._identifier == "DECIMAL":
            return Decimal()
        if self._identifier == "HEXADECIMAL":
            return Hexadecimal()
        if self._identifier == "VARIABLE":
            return Variable()
        if self._identifier == "SINGLE_COMMENT":
            return SingleComment()
