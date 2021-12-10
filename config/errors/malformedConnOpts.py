"""class malformedConnOpts"""

class malformedConnOpts(Exception):
    def __init__(self, connOpts):
        super().__init__(
            f"malformed connection options: '{connOpts}'. Please use the format 'opt1=val1,opt2=val2,...'"
        )
