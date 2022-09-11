from base_classes.value import Value
from error_classes.runtime_error import RunTimeError


class Array(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.boolean = True if self.value else False

    def set(self, idx, value):
        if str(idx).find(".") != -1:
            return 1, RunTimeError(
                self.pos_start,
                self.pos_end,
                "Expected an integer for an array index.",
                self.context,
            )
        if int(idx) < len(self.value) and int(idx) >= 0:
            self.value[int(idx)] = value
            return 0, None
        return 1, RunTimeError(
            self.pos_start, self.pos_end, "Index out of range.", self.context
        )

    def get(self, idx):
        if str(idx).find(".") != -1:
            return None, RunTimeError(
                self.pos_start,
                self.pos_end,
                "Expected an integer for an array index.",
                self.context,
            )
        if int(idx) < len(self.value) and int(idx) >= 0:
            return self.value[int(idx)], None
        return None, RunTimeError(
            self.pos_start, self.pos_end, "Index out of range.", self.context
        )

    def copy(self):
        copy = Array(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        rep_str = "["
        count_ = 0
        for tok in self.value:
            if count_ != len(self.value) - 1:
                rep_str += str(tok.__repr__()) + ","
            else:
                rep_str += str(tok.__repr__())
            count_ += 1
        rep_str += "]"
        return rep_str
