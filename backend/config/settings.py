from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    neon_db_url: str
    # Auth settings
    better_auth_secret: str
    better_auth_url: str = "http://localhost:3000"
    # API keys
    cohere_api_key: str
    # Server settings
    port: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False  # optional, case insensitive
        # Map lowercase attributes to uppercase .env keys
        fields = {
            "neon_db_url": "NEON_DB_URL",
            "better_auth_secret": "BETTER_AUTH_SECRET",
            "better_auth_url": "BETTER_AUTH_URL",
            "cohere_api_key": "COHERE_API_KEY",
            "port": "PORT"
        }

settings = Settings()

