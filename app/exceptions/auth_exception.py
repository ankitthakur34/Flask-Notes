class InvalidCredentialsException(Exception):
    def __init__(self, message="Invalid credentials",status_code=401):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ForbiddenException(Exception):

    def __init__(
        self,
        message="Access denied",
        status_code=403
    ):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)     

class EmailNotVerified(Exception):

    def __init__(
        self,
        message="email not verified",
        status_code=403
    ):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)              