from fastapi import HTTPException


class OTPCodeCreationError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Can't create OTP code!")


class InvalidOTPCodeError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Provided OTP code is not valid",
        )


class MissingRequestIDException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400, detail="Missing or expired Vonage request ID!"
        )
