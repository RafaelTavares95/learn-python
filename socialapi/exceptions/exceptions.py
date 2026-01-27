from fastapi import HTTPException


class CredentialException(HTTPException):
    def __init__(
        self,
        status: int = 401,
        message: str = "One of your information is wrong, please verify your email or password.",
    ):
        self.message = message
        self.status_code = status
        super().__init__(self.status_code, self.message)


class UnauthorizedException(HTTPException):
    def __init__(
        self,
        status: int = 401,
        message: str = "Invalid token.",
    ):
        self.message = message
        self.status_code = status
        super().__init__(self.status_code, self.message)
