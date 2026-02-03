from enum import Enum


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    CONFIRMATION = "confirmation"
    RESET_PASSWORD = "password_reset"
