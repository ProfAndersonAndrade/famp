from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR = '/api/v1'
    DB_URL : str = 'postgresql+asyncpg://andy:0Antero1@localhost:5432/faculdade'

    JWT_SECRET: str = 'DToMy9HOFaFw3X2X5iXebHBrRnU-9Pfoy2jfW4u3Z9E'
    '''
    >>>import secrets

    >>>token: str = secrets.token_urlsafe(32)

    >>>token

    '''
    ALGORITHM: str = 'HS256'
    # 60 minutos * 24 horas * 7 dias = 1 semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24*7

    class Config:
        case_sensitive = True


settings : Settings = Settings()
