from base_classes.error import Error


class UnexpectedEOLError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, "Unexpected EOL", details, context)