from pydantic_settings import BaseSettings
import secrets

class Settings(BaseSettings):
    DATABASE_URL:str ="sqlite://./test.db"
    GOOGLE_ID:str
    GOOGLE_SECRET:str
    CALLBACK_URL:str = "http://localhost:3000/api/v1/auth/callback"
    REDIRECT_URL:str = "/admin"
    SECRET:str =secrets.token_urlsafe(15)
    
    class Config:
        env_file = ".env"