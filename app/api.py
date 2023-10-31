import os

from fastapi import FastAPI, HTTPException
import redis
from httpx import Request

from .main import app
from .vonage_verify_api_manager import VonageVerifyAPIManager
from .exceptions import MissingRequestIDException, NotValidOTPCodeError, OTPCodeCreationError
from .validators import PhoneNumberValidator

app = FastAPI()


redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
vonage_manager = VonageVerifyAPIManager(
    api_key=os.getenv("VONAGE_API_KEY"),
    api_secret=os.getenv("VONAGE_API_SECRET")
)


@app.post("/2fa/init/{user_identifier}")
async def initiate_2fa(phone_number: PhoneNumberValidator) -> Request:
    try:
        verification_id = vonage_manager.request_otp(phone_number)
        redis_client.set(verification_id, phone_number)
        return {"message": "OTP sent for verification"}
    except OTPCodeCreationError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)


@app.post("/2fa/verify/{verification_id}")
async def verify_2fa(
    user_identifier: str,
    otp_code: str,
):
    request_id = redis_client.get(user_identifier)

    if not request_id:
        raise MissingRequestIDException()
    try:
        vonage_manager.verify_otp(otp_code, request_id)
        return {"message": "2FA verification successful"}
    except NotValidOTPCodeError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
