"""class emailTaken"""

class emailTaken(Exception):
    def __init__(self, email):
        return super().__init__("Email {} already taken".format(email))
