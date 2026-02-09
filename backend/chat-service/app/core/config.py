import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    LOAN_SERVICE_URL:str=os.getenv('LOAN_SERVICE_URL')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRES_MINUTES:int=os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES")
    if DATABASE_URL is None:
        raise RuntimeError("DATABASE_URL not set in the .env file")
    if LOAN_SERVICE_URL is None:
        raise RuntimeError("LOAN_SERVICE_URL not set in the .env file")
    if SECRET_KEY is None:
        raise RuntimeError("SECRET_KEY not set in the .env file")
    if ALGORITHM is None:
        raise RuntimeError("ALGORITHM not set in the .env file")
settings = Settings()
