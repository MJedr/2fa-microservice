import pytest
from utils import get_redis_client


@pytest.fixture(scope="function")
def clean_redis():
    yield
    client = get_redis_client()
    client.delete("*")
