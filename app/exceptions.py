from fastapi import HTTPException


class OTPCodeCreationError(HTTPException):
    """
    Exception raised when an OTP code cannot be created.
    """

    def __init__(self):
        super().__init__(status_code=400, detail="Can't create OTP code!")


class InvalidOTPCodeError(HTTPException):
    """
    Exception raised when the provided OTP code is not valid.
    """

    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Provided OTP code is not valid",
        )


class MissingRequestIDException(HTTPException):
    """
    Exception raised when a Vonage request ID is missing or expired.

    """

    def __init__(self):
        super().__init__(
            status_code=400, detail="Missing or expired Vonage request ID!"
        )
