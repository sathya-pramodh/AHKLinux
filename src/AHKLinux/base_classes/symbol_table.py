class SymbolTable:
    def __init__(self, symbols={}):
        self.symbols = symbols
        self.parent = None

    def get(self, name):
        value = self.symbols.get(name, None)
        if value is None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value, global_=False):
        if global_ and self.parent is not None:
            self.parent.symbols[name] = value
        else:
            self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]
