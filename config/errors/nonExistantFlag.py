"""class nonExistantFlag"""

class nonExistantFlag(Exception):
    def __init__(self, cliArgument):
        super().__init__(
            f"the flag '{cliArgument}' was specified but does not match any of the valid flags"
        )
