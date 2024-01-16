from enum import Enum


class SessionLogin(Enum):
    EMAIL = "Sign in to X"
    USERNAME = "Enter your phone number or username"
    PASSWORD = "Enter your password"
    VERIFICATION_CODE = "Enter your verification code"
