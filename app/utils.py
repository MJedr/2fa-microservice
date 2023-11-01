import os
from vonage_verify_api_manager import VonageVerifyAPIManager
import redis
from config import Settings
from functools import lru_cache


@lru_cache
def get_settings():
    return Settings()


def get_vonage_api_manager():
    """
    Returns an instance of the VonageVerifyAPIManager class, which is used to interact with the Vonage Verify API.

    Returns:
    An instance of the VonageVerifyAPIManager class.
    """
    settings = get_settings()
    vonage_manager = VonageVerifyAPIManager(
        api_key=settings.VONAGE_API_KEY,
        api_secret=settings.VONAGE_API_SECRET,
        root_vonage_url=settings.VONAGE_API_ROOT_URL,
        brand_name=settings.VONAGE_API_BRAND_NAME,
    )
    return vonage_manager


def get_redis_client():
    """
    Returns a Redis client instance.

    :return: Redis client instance.
    """
    settings = get_settings()
    client = redis.StrictRedis(
        host=settings.REDIS_CLIENT_HOST,
        port=settings.REDIS_CLIENT_PORT,
        decode_responses=True,
        db=0,
    )
    return client
