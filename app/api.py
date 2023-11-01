from exceptions import (
    InvalidOTPCodeError,
    MissingRequestIDException,
    OTPCodeCreationError,
)
from fastapi import APIRouter
from serializers import PhoneNumber, VerifyRequestData
from utils import get_redis_client, get_vonage_api_manager

redis_client = get_redis_client()
router = APIRouter()


@router.post("/init")
async def initiate_2fa(phone_number: PhoneNumber):
    """
    Initiates the 2-factor authentication process by sending an OTP to the provided phone number.

    Args:
        phone_number (PhoneNumber): The phone number to which the OTP will be sent.

    Raises:
        OTPCodeCreationError: If OTP creation failed.

    Returns:
        dict: A dictionary containing a message indicating that the OTP has been sent for verification.
    """
    validated_phone_number = phone_number.phone_number
    try:
        manager = get_vonage_api_manager()
        verification_id = await manager.request_otp(validated_phone_number)
        redis_client.set(validated_phone_number, verification_id)
        return {"message": "OTP sent for verification"}
    except OTPCodeCreationError:
        raise


@router.post("/verify")
async def verify_2fa(request_data: VerifyRequestData):
    """Verify the 2FA code for a given phone number.

    Args:
        request_data (VerifyRequestData): The request data containing the phone number and OTP code.

    Raises:
        MissingRequestIDException: If the request ID is missing from Redis.
        InvalidOTPCodeError: If the OTP validation was not successful.

    Returns:
        dict: A dictionary containing a success message if the verification is successful.
    """
    validated_phone_number = request_data.phone_number
    request_id = redis_client.get(validated_phone_number)

    if not request_id:
        raise MissingRequestIDException()
    try:
        manager = get_vonage_api_manager()
        await manager.verify_otp(otp_code=request_data.otp_code, request_id=request_id)
        return {"message": "2FA verification successful"}
    except InvalidOTPCodeError:
        raise
