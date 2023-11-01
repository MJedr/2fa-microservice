import mock
import pytest
from exceptions import InvalidOTPCodeError, OTPCodeCreationError
from httpx import Response
from vonage_verify_api_manager import VonageVerifyAPIManager


@pytest.fixture(autouse=True)
def vonage_verify_manager_mock() -> VonageVerifyAPIManager:
    api_key = "test"
    api_secret = "test"
    root_vonage_url = "https://example.com"
    return VonageVerifyAPIManager(api_key, api_secret, root_vonage_url)


@pytest.mark.asyncio
@mock.patch.object(VonageVerifyAPIManager, "http_client")
async def test_request_otp_happy_flow(http_client_mock, vonage_verify_manager_mock):
    expected_request_id = "1234"
    mock_response = Response(200)
    mock_response.json = mock.Mock(return_value={"request_id": "1234"})

    async def mocked_post_request(endpoint, data):
        return mock_response

    http_client_mock.post_request.side_effect = mocked_post_request

    phone_number = "+48666777888"
    request_id = await vonage_verify_manager_mock.request_otp(phone_number)

    assert request_id == expected_request_id


@pytest.mark.asyncio
@mock.patch.object(VonageVerifyAPIManager, "http_client")
async def test_request_otp_failure(http_client_mock, vonage_verify_manager_mock):
    mock_response = Response(404)
    mock_response.json = mock.Mock(return_value={"request_id": "1234"})

    async def mocked_post_request(endpoint, data):
        return mock_response

    http_client_mock.post_request.side_effect = mocked_post_request

    phone_number = "+48666777888"
    with pytest.raises(OTPCodeCreationError):
        await vonage_verify_manager_mock.request_otp(phone_number)


@pytest.mark.asyncio
@mock.patch.object(VonageVerifyAPIManager, "http_client")
async def test_verify_otp_failure(http_client_mock, vonage_verify_manager_mock):
    mock_response = Response(404)
    mock_response.json = mock.Mock(return_value={"detail": "Error detail"})

    async def mocked_post_request(endpoint, data):
        return mock_response

    http_client_mock.post_request.side_effect = mocked_post_request

    request_id = "123456"
    otp_code = "1234"

    with pytest.raises(InvalidOTPCodeError):
        await vonage_verify_manager_mock.verify_otp(request_id, otp_code)


@pytest.mark.asyncio
@mock.patch.object(VonageVerifyAPIManager, "http_client")
async def test_verify_otp_happy_flow(http_client_mock, vonage_verify_manager_mock):
    mock_response = Response(200)
    mock_response.json = mock.Mock(return_value=None)

    async def mocked_post_request(endpoint, data):
        return mock_response

    http_client_mock.post_request.side_effect = mocked_post_request

    request_id = "123456"
    otp_code = "1234"
    result = await vonage_verify_manager_mock.verify_otp(request_id, otp_code)

    assert result
