from pydantic_settings import BaseSettings


class Config(BaseSettings):
    token_expiry: int = 60 * 24  # minutes
    jwt_secret: str = "jwt"


config = Config()
