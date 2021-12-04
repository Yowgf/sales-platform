"""InvalidValue class"""

class InvalidValue(Exception):
    def __init__(self, attributeName, validLengthRange):
        super().__init__(
            "value of {} has to be in the range ({}, {})".format(
                attributeName, validLengthRange[0], validLengthRange[1]
            )
        )
