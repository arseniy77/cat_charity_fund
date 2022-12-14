from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Кошачьи инвестиции'
    database_url: str = 'sqlite+aiosqlite:///./database.db'
    secret: str = 'secret'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    description: str = 'Описание'
    token_lifetime: int = 3600

    class Config:
        env_file = '.env'


settings = Settings()
