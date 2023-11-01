import os

import redis
from exceptions import (
    InvalidOTPCodeError,
    MissingRequestIDException,
    OTPCodeCreationError,
)
from fastapi import HTTPException, APIRouter
from httpx import Request
from validators import PhoneNumberValidator, VerifyRequestData
from vonage_verify_api_manager import VonageVerifyAPIManager

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)
vonage_manager = VonageVerifyAPIManager(
    api_key=os.getenv("VONAGE_API_KEY"), api_secret=os.getenv("VONAGE_API_SECRET")
)

router = APIRouter()

@router.post("/init")
async def initiate_2fa(phone_number: PhoneNumberValidator):
    try:
        verification_id = vonage_manager.request_otp(phone_number)
        # TODO: sanitaze phone nr somehow
        redis_client.set(verification_id, phone_number)
        return {"message": "OTP sent for verification"}
    except OTPCodeCreationError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)


@router.post("/verify")
async def verify_2fa(
     request_data: VerifyRequestData
):

    request_id = redis_client.get(request_data.phone_number)

    if not request_id:
        raise MissingRequestIDException()
    try:
        vonage_manager.verify_otp(request_data.otp_code, request_id)
        return {"message": "2FA verification successful"}
    except InvalidOTPCodeError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
