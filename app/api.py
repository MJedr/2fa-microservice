import os

import redis
from exceptions import (
    InvalidOTPCodeError,
    MissingRequestIDException,
    OTPCodeCreationError,
)
from fastapi import APIRouter, HTTPException
from httpx import Request
from serializers import PhoneNumber, VerifyRequestData
from utils import get_redis_client, get_vonage_api_manager
from vonage_verify_api_manager import VonageVerifyAPIManager

redis_client = get_redis_client()
router = APIRouter()


# @app.exception_handler(RequestValidationError)
# @app.exception_handler(ValidationError)
# async def validation_exception_handler(request, exc):
#     print(f"OMG! The client sent invalid data!: {exc}")
#     exc_json = json.loads(exc.json())
#     response = {"message": [], "data": None}
#     for error in exc_json:
#         response['message'].append(error['loc'][-1]+f": {error['msg']}")

#     return JSONResponse(response, status_code=422)


@router.post("/init")
async def initiate_2fa(phone_number: PhoneNumber):
    validated_phone_number = phone_number.phone_number
    try:
        manager = get_vonage_api_manager()
        verification_id = await manager.request_otp(validated_phone_number)
        redis_client.set(validated_phone_number, verification_id)
        return {"message": "OTP sent for verification"}
    except OTPCodeCreationError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)


@router.post("/verify")
async def verify_2fa(request_data: VerifyRequestData):
    validated_phone_number = request_data.phone_number
    request_id = redis_client.get(validated_phone_number)

    if not request_id:
        raise MissingRequestIDException()
    try:
        manager = get_vonage_api_manager()
        await manager.verify_otp(otp_code=request_data.otp_code, request_id=request_id)
        return {"message": "2FA verification successful"}
    except InvalidOTPCodeError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
