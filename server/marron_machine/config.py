from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets
from datetime import timedelta as _timedelta

class Settings(BaseSettings):
    DATABASE_URL:str ="sqlite://./test.db"
    CALLBACK_URL:str = "http://localhost:3000/api/v1/auth/callback"
    SECRET:str =secrets.token_urlsafe(15)
    TZ:str = "Asia/Tokyo"
    TOKEN_EXPIRE:_timedelta = _timedelta(hours=1)
    SERVE_STATIC:Optional[str]=None
    
    model_config = SettingsConfigDict(env_file=".env")