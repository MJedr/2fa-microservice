import logging
from tenacity import retry, stop_after_attempt, retry_if_exception_type
from functools import cached_property

from exceptions import InvalidOTPCodeError, OTPCodeCreationError
from httpx import AsyncClient, Response, ConnectTimeout
from serializers import PhoneNumber

logger = logging.getLogger(__name__)


class VonageHTTPClient:
    """
    A client for making HTTP requests to the Vonage Verify API.

    Parameters
    ----------
    base_url : str
        The base URL for the Vonage Verify API.
    api_key : str
        The API key to use for authentication.
    api_secret : str
        The API secret to use for authentication.
    """

    def __init__(self, base_url: str, api_key: str, api_secret: str):
        self.base_url = base_url
        self.api_key = api_key
        self.api_secret = api_secret

    @retry(retry=retry_if_exception_type(ConnectTimeout), stop=stop_after_attempt(5))
    async def post_request(self, endpoint: str, data: dict) -> Response:
        """
        Sends a POST request to the Vonage Verify API with the given endpoint and data.

        Parameters
        ----------
        endpoint : str
            the endpoint to send the request to
        data : dict
            the data to include in the request body

        Returns
        -------
        Response
            the response object returned by the Vonage Verify API

        """
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
        """
        Initializes a new instance of the VonageVerifyAPIManager class.

        Args:
            api_key (str): The Vonage API key to use.
            api_secret (str): The Vonage API secret to use.
            root_vonage_url (str): The root URL of the Vonage API to use.
            brand_name (str): The name of the brand to use when sending verification messages.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = root_vonage_url
        self.brand_name = brand_name

    @cached_property
    def http_client(self) -> VonageHTTPClient:
        """
        Returns an instance of VonageHTTPClient, which is used to make HTTP requests to the Vonage Verify API.

        :return: An instance of VonageHTTPClient.
        """
        return VonageHTTPClient(
            api_key=self.api_key, api_secret=self.api_secret, base_url=self.base_url
        )

    def _get_otp_request_payload(self, phone_number) -> dict:
        """
        Returns the request payload for requesting an OTP code for the given phone number.

        Args:
            phone_number (PhoneNumber): The phone number to request the OTP code for.

        Returns:
            dict: The request payload.
        """
        request_data = {
            "brand": "Test",
            "workflow": [{"channel": "sms", "to": phone_number}],
        }
        return request_data

    async def request_otp(self, phone_number: PhoneNumber) -> str:
        """
        Requests a one-time password (OTP) code for the given phone number.

        Args:
            phone_number (PhoneNumber): The phone number to request the OTP code for.

        Raises:
            OTPCodeCreationError: If there was an error creating the OTP code.

        Returns:
            str: The request ID for the OTP code.
        """
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
        """
        Verify an OTP code for a given request ID.

        Args:
            request_id (str): The ID of the request to verify the OTP code for.
            otp_code (str): The OTP code to verify.

        Raises:
            InvalidOTPCodeError: If the OTP code is invalid.

        Returns:
            bool: True if the OTP code is valid, False otherwise.
        """
        request_data = {"code": otp_code}
        response = await self.http_client.post_request(
            endpoint=f"/verify/{request_id}",
            data=request_data,
        )
        if response.is_success:
            return True
        else:
            message = response.json().get("detail", "Unknown error")
            logger.error(
                f"Request failed with status code {response.status_code}. Message: {message}"
            )
            raise InvalidOTPCodeError()
