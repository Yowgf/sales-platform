"""class missingFlags"""

class missingFlags(Exception):
    def __init__(self, missingFlagsMessage):
        super().__init__(
            f"missing required flags: '{missingFlagsMessage}'"
        )
