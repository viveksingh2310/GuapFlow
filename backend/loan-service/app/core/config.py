import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = os.getenv('ALGORITHM')
    ACCOUNT_SERVICE_URL=os.getenv('ACCOUNT_SERVICE_URL')
    if DATABASE_URL is None:
        raise RuntimeError("DATABASE_URL not set in the .env file")
    if SECRET_KEY is None:
        raise RuntimeError("SECRET_KEY not set in the .env file")
    if ALGORITHM is None:
        raise RuntimeError("ALGORITHM not set in the .env file")
    if ACCOUNT_SERVICE_URL is None:
        raise RuntimeError("ACCOUNT_SERVICE_URL not set in the .env file")
settings = Settings()