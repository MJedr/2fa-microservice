import logging
import os
from functools import cached_property

from exceptions import InvalidOTPCodeError, OTPCodeCreationError
from httpx import AsyncClient, Response
from validators import PhoneNumberValidator

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
                data=data,
                auth=(self.api_key, self.api_secret),
            )
            return response


class VonageVerifyAPIManager:
    def __init__(self, api_key: str, api_secret: str, root_vonage_url: str = None) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = root_vonage_url or os.getenv("ROOT_VONAGE_URL")

    @property
    def url_map(self):
        return {"new_request": "/newRequest", "verify_request": "/checkCode-auth"}

    @cached_property
    def http_client(self):
        return VonageHTTPClient(self.api_key, self.api_secret, self.base_url)

    async def request_otp(self, phone_number: PhoneNumberValidator) -> str:
        request_data = {
            "brand": "YourBrandName",
            "workflow": [{"channel": "sms", "to": phone_number}],
        }

        response = self.http_client.post_request(
            endpoint=self.url_map["new_request"], data=request_data
        )
        if response.status_code == 200:
            return response.json()["request_id"]
        else:
            message = response.json().get("detail", "Unknown error")
            logger.error(
                f"Request failed with status code {response.status_code}. Message: {message}"
            )
            raise OTPCodeCreationError()

    async def verify_otp(self, request_id: str, otp_code: str) -> bool:
        request_data = {"code": otp_code}
        response = self.http_client.post_request(
            endpoint=self.url_map["verify_request"] + f"/{request_id}",
            data=request_data,
        )
        if response.status_code == 200:
            return
        else:
            message = response.json().get("detail", "Unknown error")
            logger.error(
                f"Request failed with status code {response.status_code}. Message: {message}"
            )
            raise InvalidOTPCodeError()
