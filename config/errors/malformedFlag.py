"""class malformedFlag"""

class malformedFlag(Exception):
    def __init__(self, cliArgument):
        super().__init__(
            f"the flag '{cliArgument}' is malformed. Please use the format 'flag=value'"
        )
