import pytest
from validators import PhoneNumberValidator


@pytest.mark.parametrize("phone_number",[
        "12345",
        "54321",
        "9876543210",
        "12345678901234",
        "123456789012345",
    ]
)
def test_valid_phone_number(phone_number):
    assert PhoneNumberValidator(phone_number=phone_number)


@pytest.mark.parametrize("phone_number",[
        "",
        "+",
        "+0",
        "1234 5678",
        "1234-5678",
        "1a23456789",
        "1234567890123456",
    ] )
def test_invalid_phone_number(phone_number):
    with pytest.raises(ValueError):
        PhoneNumberValidator(phone_number=phone_number)


def test_strip_plus_sign():
    phone_number_with_plus = PhoneNumberValidator(phone_number="+12345")
    phone_number_without_plus = PhoneNumberValidator(phone_number="12345")
    
    assert phone_number_with_plus.phone_number == "12345"
    assert phone_number_without_plus.phone_number == "12345"
