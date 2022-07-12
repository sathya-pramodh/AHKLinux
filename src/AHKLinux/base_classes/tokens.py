class Token:
    """
    A Token base class to represent all the tokens in the AutoHotKey script.
    """

    def __init__(self, identifier, name):
        self._identifier = identifier
        self._name = name
