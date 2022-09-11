from base_classes.value import Value


class Boolean(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.boolean = True if self.value == "true" else False

    def compare(self, other, operator):
        if operator == "and":
            result = self.boolean and other.boolean
            if result:
                return Boolean("true")
            return Boolean("false")
        elif operator == "or":
            result = self.boolean or other.boolean
            if result:
                return Boolean("true")
            return Boolean("false")

    def copy(self):
        copy = Boolean(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f"{self.value}"
