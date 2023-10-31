from fastapi import HTTPException


class OTPCodeCreationError(HTTPException):
    status_code = 400
    detail = "Can't create OTP code!"


class NotValidOTPCodeError(HTTPException):
    status_code = 400
    detail = "Provided OTP code is not validated by the validation server"

 
class MissingRequestIDException(HTTPException):
    status_code = 500
    detail = "Missing or expired Vonage request ID!"


class MissingRequestIDException(HTTPException):
    status_code = 401
    detail = "Invalid OTP Password"
