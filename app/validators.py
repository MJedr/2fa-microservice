import re
from pydantic import BaseModel, validator


class PhoneNumberValidator(BaseModel):
    phone_number: str

    @validator("phone_number")
    def validate_phone_number(cls, value):
        phone_number_regex = r'^\+?[0-9()-.\s]+$'  # This is a simplification, can be adjusted according to business requirements
        if not re.match(phone_number_regex, value):
            raise ValueError("Invalid phone number format")

        return value
