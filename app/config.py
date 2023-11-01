from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv("app/env/.env-local")


class Settings(BaseSettings):
    VONAGE_API_KEY: str = "test"
    VONAGE_API_SECRET: str = "test"
    VONAGE_API_ROOT_URL: str = "https://api.nexmo.com/v2"
    VONAGE_API_BRAND_NAME: str = "Test"
    REDIS_CLIENT_HOST: str = "localhost"
    REDIS_CLIENT_PORT: int = 6379
    REDIS_CLIENT_KEY_EXPIRATION_SEC: int = 60 * 3  # the time OTP is active

    model_config = SettingsConfigDict(case_sensitive=True)
