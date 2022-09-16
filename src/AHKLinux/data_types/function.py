from base_classes.value import Value


class Function(Value):
    def __init__(self, name, parameters, statements):
        super().__init__()
        self.name = name
        self.parameters = parameters
        self.statements = statements

    def __repr__(self):
        return r"{}({}){{}}".format(self.name, self.parameters, self.statements)
