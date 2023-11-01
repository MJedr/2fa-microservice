import os
from vonage_verify_api_manager import VonageVerifyAPIManager
import redis


def get_vonage_api_manager():
    vonage_manager = VonageVerifyAPIManager(
        api_key=os.getenv("VONAGE_API_KEY"), api_secret=os.getenv("VONAGE_API_SECRET")
    )
    return vonage_manager


def get_redis_client():
    client = redis.StrictRedis(
        host=os.getenv('REDIS_CLIENT_HOST', 'localhost'),
        port=os.getenv('REDIS_CLIENT_PORT', '6379'),
        db=0
    )
    return client
