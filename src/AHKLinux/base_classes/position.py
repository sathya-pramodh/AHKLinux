class Position:
    def __init__(self, filename, idx, line, column, ftext):
        self.filename = filename
        self.idx = idx
        self.line = line
        self.column = column
        self.ftext = ftext

    def advance(self, current_char=None):
        self.idx += 1
        self.column += 1

        if current_char == "\n":
            self.line += 1
            self.column = 1

        return self

    def copy(self):
        return Position(self.filename, self.idx, self.line, self.column, self.ftext)
