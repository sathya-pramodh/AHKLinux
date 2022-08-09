class Error:
    def __init__(self, pos_start, pos_end, error_name, details, context):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += "{}: {}\n".format(self.error_name, self.details)
        return result

    def generate_traceback(self):
        result = ""
        pos = self.pos_start
        context = self.context

        while context:
            if pos.line == 0:
                result += "  File : '{}', line {}, in {}\n".format(
                    pos.filename, 1, context.display_name
                )
            else:
                result += "  File: '{}', line {}, in {}\n".format(
                    pos.filename, pos.line - 1, context.display_name
                )
            result += "    {}\n".format(pos.ftext.strip().split("\n")[0])
            pos = context.parent_entry_pos
            context = context.parent

        return "Traceback (most recent call last):\n" + result
