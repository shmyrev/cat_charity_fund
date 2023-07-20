from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):

    app_title: str = 'Благотворительный фонд поддержки котиков QRKot'
    app_description: str = 'Фонд собирает пожертвования на различные проекты.'
    database_url: str = 'sqlite+aiosqlite:///./cat_charity_fund.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
