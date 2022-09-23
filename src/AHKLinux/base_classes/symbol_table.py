class SymbolTable:
    def __init__(self, symbols={}):
        self.symbols = symbols
        self.parent = None

    def get(self, name):
        for name_, value_ in self.symbols.items():
            if name_.lower() == name.lower():
                return self.symbols[name_][0]

    def set(self, name, value):
        for name_ in self.symbols.keys():
            if name_.lower() == name.lower():
                self.symbols[name_] = value
                break
        else:
            self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

    def global_from_child(self, name):
        for name_ in self.symbols.keys():
            if name_.lower() == name.lower():
                return self.symbols[name_][1]
        return False
