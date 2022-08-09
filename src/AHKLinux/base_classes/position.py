class Position:
    def __init__(self, filename, idx, line, ftext):
        self.filename = filename
        self.idx = idx
        self.line = line
        self.ftext = ftext

    def advance(self):
        self.idx += 1
        return self

    def copy(self):
        return Position(self.filename, self.idx, self.line, self.ftext)
