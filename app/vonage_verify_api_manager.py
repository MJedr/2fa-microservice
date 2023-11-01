import logging
import os
from functools import cached_property

from exceptions import InvalidOTPCodeError, OTPCodeCreationError
from httpx import AsyncClient, Response
from serializers import PhoneNumber

logger = logging.getLogger(__name__)


class VonageHTTPClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url

    async def post_request(self, endpoint: str, data: dict) -> Response:
        headers = {
            "Content-Type": "application/json",
        }

        async with AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}{endpoint}",
                headers=headers,
                json=data,
                auth=(self.api_key, self.api_secret),
            )
            return response


class VonageVerifyAPIManager:
    def __init__(
        self,
        api_key: str = None,
        api_secret: str = None,
        root_vonage_url: str = None,
        brand_name: str = None,
    ) -> None:
        self.api_key = api_key or os.getenv("VONAGE_API_KEY")
        self.api_secret = api_secret or os.getenv("VONAGE_API_SECRET")
        self.base_url = root_vonage_url or os.getenv("VONAGE_API_ROOT_URL")
        self.brand_name = brand_name or os.getenv("VONAGE_API_BRAND_NAME")

    @cached_property
    def http_client(self) -> VonageHTTPClient:
        return VonageHTTPClient(self.api_key, self.api_secret, self.base_url)

    def _get_otp_request_payload(self, phone_number) -> dict:
        request_data = {
            "brand": "Test",
            "workflow": [{"channel": "sms", "to": phone_number}],
        }
        return request_data

    async def request_otp(self, phone_number: PhoneNumber) -> str:
        request_data = self._get_otp_request_payload(phone_number)

        response = await self.http_client.post_request(
            endpoint="/verify", data=request_data
        )
        if response.is_success:
            return response.json()["request_id"]
        else:
            message = response.json().get("detail", "Unknown error")
            logger.error(
                f"Request failed with status code {response.status_code}. Message: {message}"
            )
            raise OTPCodeCreationError()

    async def verify_otp(self, request_id: str, otp_code: str) -> bool:
        request_data = {"code": otp_code}
        response = await self.http_client.post_request(
            endpoint=f"/verify/{request_id}",
            data=request_data,
        )
        if response.is_success:
            return
        else:
            message = response.json().get("detail", "Unknown error")
            logger.error(
                f"Request failed with status code {response.status_code}. Message: {message}"
            )
            raise InvalidOTPCodeError()
