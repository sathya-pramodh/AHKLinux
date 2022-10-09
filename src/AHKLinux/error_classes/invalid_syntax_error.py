from base_classes.error import Error


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details, context) -> None:
        super().__init__(pos_start, pos_end, "Invalid Syntax", details, context)
