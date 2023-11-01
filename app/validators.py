import re
from pydantic import BaseModel, validator


class PhoneValidationMixin:
    @validator("phone_number", pre=True)
    def strip_plus_sign(cls, value):
        value = value.lstrip('+')
        return value

    @validator("phone_number")
    def validate_phone_number(cls, value):
        e164_phone_number_regex = r'^[1-9][0-9]{1,14}$'  # This is a simplification, can be adjusted according to business requirements
        if not re.match(e164_phone_number_regex, value):
            raise ValueError("Invalid phone number format")
        return value


class PhoneNumberValidator(BaseModel, PhoneValidationMixin):
    phone_number: str


class VerifyRequestData(BaseModel, PhoneValidationMixin):
    phone_number: str
    otp_code: str
