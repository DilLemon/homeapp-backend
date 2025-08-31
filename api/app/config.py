from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://homeapp:change@db:5432/homeapp"
    JWT_SECRET: str = "change_me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200
    DEFAULT_CURRENCY: str = "RUB"
    ERIK_PASSWORD: str = "erik"
    POLINA_PASSWORD: str = "polina"

settings = Settings()
