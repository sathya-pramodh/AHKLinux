from base_classes.error import Error


class RunTimeError(Error):
    def __init__(self, pos_start, pos_end, details, context) -> None:
        super().__init__(pos_start, pos_end, "Runtime Error", details, context)
