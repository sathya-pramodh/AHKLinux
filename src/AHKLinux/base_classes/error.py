from base_classes.context import Context
from base_classes.position import Position


class Error:
    def __init__(
        self,
        pos_start: Position,
        pos_end: Position,
        error_name: str,
        details: str,
        context: Context,
    ) -> None:
        self.pos_start: Position = pos_start
        self.pos_end: Position = pos_end
        self.error_name: str = error_name
        self.details: str = details
        self.context: Context = context

    def as_string(self) -> str:
        result: str = self.generate_traceback()
        result += "{}: {}\n".format(self.error_name, self.details)
        return result

    def generate_traceback(self) -> str:
        result: str = ""
        pos: Position = self.pos_start
        context: Context = self.context

        def get_call_stack(
            context: Context | None, pos: Position | None, result: str
        ) -> str:
            if not context or not pos:
                return result
            result = get_call_stack(context.parent, context.parent_entry_pos, result)
            result += " File: '{}', line {}, in {}\n".format(
                pos.filename, pos.line, context.display_name
            )
            result += "   {}\n".format(
                pos.ftext.strip().split("\n")[pos.line - 1].strip()
            )
            return result

        result = get_call_stack(context, pos, result)

        return "Traceback (most recent call last):\n" + result
