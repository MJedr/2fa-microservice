import os
from vonage_verify_api_manager import VonageVerifyAPIManager
import redis


def get_vonage_api_manager():
    """
    Returns an instance of the VonageVerifyAPIManager class, which is used to interact with the Vonage Verify API.

    Returns:
    An instance of the VonageVerifyAPIManager class.
    """
    vonage_manager = VonageVerifyAPIManager()
    return vonage_manager


def get_redis_client():
    """
    Returns a Redis client instance.

    :return: Redis client instance.
    """
    client = redis.StrictRedis(
        host=os.getenv('REDIS_CLIENT_HOST', 'localhost'),
        port=os.getenv('REDIS_CLIENT_PORT', '6379'),
        db=0
    )
    return client
