from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CANVAS_API_BASE_URL: str = "https://canvas.instructure.com/api/v1"
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()