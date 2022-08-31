class Position:
    def __init__(self, filename, idx, line, ftext):
        self.filename = filename
        self.idx = idx
        self.line = line
        self.ftext = ftext

    def advance(self, current_char):
        self.idx += 1
        if current_char == "\n":
            self.line += 1
        return self

    def copy(self):
        return Position(self.filename, self.idx, self.line, self.ftext)
