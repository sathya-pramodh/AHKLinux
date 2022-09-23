from base_classes.value import Value
from data_types.boolean import Boolean


class Function(Value):
    def __init__(self, name, parameters, body):
        super().__init__()
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return r"{}({}){{}}".format(self.name, self.parameters, self.body)
