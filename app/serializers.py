import re

from pydantic import BaseModel, validator


class PhoneValidationMixin:
    """
    A mixin class that provides phone number validation functionality.

    This mixin class provides two validators for the `phone_number` field:
    - `strip_plus_sign`: strips any leading plus sign from the phone number.
    - `validate_phone_number`: validates that the phone number is in E.164 format.

    Example usage:
    ```
    class MySerializer(PhoneValidationMixin, serializers.Serializer):
        phone_number = serializers.CharField()
    ```
    """
    @validator("phone_number", pre=True)
    def strip_plus_sign(cls, value):
        value = value.lstrip("+")
        return value

    @validator("phone_number")
    def validate_phone_number(cls, value):
        e164_phone_number_regex = r"^[1-9][0-9]{1,14}$"
        if not re.match(e164_phone_number_regex, value):
            raise ValueError("Invalid phone number format")
        return value


class PhoneNumber(BaseModel, PhoneValidationMixin):
    """
    A class representing a phone number.

    Attributes:
    -----------
    phone_number : str
        The phone number to be validated.
    """
    phone_number: str


class VerifyRequestData(BaseModel, PhoneValidationMixin):
    """
    A data model for verifying a user's phone number with an OTP code.

    Attributes:
    -----------
    phone_number : str
        The user's phone number to be verified.
    otp_code : str
        The OTP code to be used for verification.
    """
    phone_number: str
    otp_code: str
