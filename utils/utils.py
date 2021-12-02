from datetime import datetime

from errors.InvalidLength import InvalidLength

class datetimeNow():
    def __init__(self):
        self.dt = datetime.now()

    def formalStr(self):
        return self.dt.isoformat()

    def prettyStr(self):
        return self.dt.strftime("%A, %d. %B %Y %I:%M%p")

# True if in range, false otherwise
def inRange(val, rng):
    return rng[0] <= val and val <= rng[1]
    
def checkAttLenInRange(attName, val, rng):
    if not inRange(len(val), rng):
        raise InvalidLength(attName, rng)
