import mock

from fastapi.testclient import TestClient
from main import app


@mock.patch("vonage_verify_api_manager.VonageVerifyAPIManager")
@mock.patch("api.redis.StrictRedis.set", return_value="OK")
def test_initiate_2fa_success(redis_set_mock, vonage_manager_mock):
    client = TestClient(app)
    response = client.post(
        "/2fa/init", json={"phone_number": "+12345678"}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "OTP sent for verification"}

    assert redis_set_mock.called

@mock.patch("vonage_verify_api_manager.VonageVerifyAPIManager")
@mock.patch("api.redis.StrictRedis.get", return_value="12345678")
def test_verify_2fa_success(redis_get_mock, vonage_manager_mock):
    client = TestClient(app)
    response = client.post("/2fa/verify", json={"phone_number": "+12345678", "otp_code": "1234aq"})


    assert response.status_code == 200
    assert response.json() == {"message": "2FA verification successful"}
