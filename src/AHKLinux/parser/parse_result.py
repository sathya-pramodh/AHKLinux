class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def __repr__(self):
        return f"{self.node}"

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self
