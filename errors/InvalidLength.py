"""InvalidLength class

The error InvalidLength is raised when some function parameter has invalid
length.

Notice that the error message here has to be user-facing, so it should only
include useful information for the user.
"""

class InvalidLength(Exception):
    def __init__(self, attributeName, validLengthRange):
        super().__init__(
            "the length of {} has to be in the range ({}, {})".format(
                attributeName, validLengthRange[0], validLengthRange[1]
            )
        )
