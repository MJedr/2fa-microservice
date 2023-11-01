import mock
import pytest
from fastapi.testclient import TestClient
from main import app


def scrub_phone_number(request):
    request.body = ''
    return request


@pytest.mark.vcr(
    filter_headers=["authorization", "Set-Cookie"],
    before_record_request=scrub_phone_number
)
def test_integration_init_and_verify_happy_flow(clean_redis):
    client = TestClient(app)

    otp_code = "1234"

    with mock.patch(
        "vonage_verify_api_manager.VonageVerifyAPIManager._get_otp_request_payload"
    ) as mock_get_payload:
        expected_payload = {
            "brand": "Test",
            "code": otp_code,
            "workflow": [{"channel": "sms", "to": "+48666777888"}],
        }

        mock_get_payload.return_value = expected_payload
        init_response = client.post("/2fa/init", json={"phone_number": "+12345678"})

        assert init_response.status_code == 200
        assert init_response.json() == {"message": "OTP sent for verification"}

        verify_response = client.post(
            "/2fa/verify", json={"phone_number": "+12345678", "otp_code": otp_code}
        )

        assert verify_response.status_code == 200
        assert verify_response.json() == {"message": "2FA verification successful"}


@pytest.mark.vcr(
    filter_headers=["authorization", "Set-Cookie"],
    before_record_request=scrub_phone_number
)
def test_integration_2fa_init_not_authenticated(clean_redis):
    client = TestClient(app)
    init_response = client.post("/2fa/init", json={"phone_number": "+12345678"})

    assert init_response.status_code == 400
    assert init_response.json() == {'detail': "Can't create OTP code!"}


@pytest.mark.vcr(
    filter_headers=["authorization", "Set-Cookie"],
    before_record_request=scrub_phone_number
)
def test_integration_2fa_verify_not_authenticated(clean_redis):
    client = TestClient(app)
    init_response = client.post("/2fa/verify", json={"phone_number": "+12345678", "otp_code": '1234'})

    assert init_response.status_code == 400
    assert init_response.json() == {'detail': 'Incorrect or expired Vonage request ID!'}


@pytest.mark.vcr(
    filter_headers=["authorization", "Set-Cookie"],
    before_record_request=scrub_phone_number
)
def test_integration_init_and_verify_2fa_wrong_otp_code(clean_redis):
    client = TestClient(app)

    otp_code = "thisisawrongcode"
    init_response = client.post("/2fa/init", json={"phone_number": "+48666777888"})

    assert init_response.status_code == 200
    assert init_response.json() == {"message": "OTP sent for verification"}

    verify_response = client.post(
        "/2fa/verify", json={"phone_number": "+48666777888", "otp_code": otp_code}
    )

    assert verify_response.status_code == 400
    assert verify_response.json() == {'detail': 'Provided OTP code is not valid'}
