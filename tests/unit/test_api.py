import mock
from fastapi.testclient import TestClient
from main import app
from mock import MagicMock


@mock.patch(
    "vonage_verify_api_manager.VonageVerifyAPIManager.request_otp",
    return_value="1234a",
)
@mock.patch("api.redis_client", return_value=MagicMock())
def test_initiate_2fa_success(redis_mock, vonage_manager_mock):
    client = TestClient(app)
    response = client.post("/2fa/init", json={"phone_number": "+12345678"})

    assert response.status_code == 200
    assert response.json() == {"message": "OTP sent for verification"}

    assert redis_mock.set.called


@mock.patch(
    "vonage_verify_api_manager.VonageVerifyAPIManager.verify_otp", return_value=True
)
@mock.patch("api.redis_client", return_value=MagicMock())
def test_verify_2fa_success(redis_mock, vonage_manager_mock):
    client = TestClient(app)
    redis_mock.get.return_value = "1234"
    mock.patch("api.get_redis_client", return_value=redis_mock)

    response = client.post(
        "/2fa/verify", json={"phone_number": "+12345678", "otp_code": "1234aq"}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "2FA verification successful"}
    assert redis_mock.get.called
