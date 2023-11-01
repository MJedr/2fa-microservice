from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    VONAGE_API_KEY: str
    VONAGE_API_SECRET: str
    VONAGE_API_ROOT_URL: str
    VONAGE_API_BRAND_NAME: str
    REDIS_CLIENT_HOST: str
    REDIS_CLIENT_PORT: int

    model_config = SettingsConfigDict(env_file=".env")
