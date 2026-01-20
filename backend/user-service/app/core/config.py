import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str= os.getenv("SECRET_KEY")
    ALGORITHM:str=os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRES_MINUTES:int=os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES")
    ROLE_ADMIN:str=os.getenv("ROLE_ADMIN")
    ROLE_USER:str=os.getenv("ROLE_USER")
    if DATABASE_URL is None:
        raise RuntimeError("DATABASE_URL is not set in .env file")
    if SECRET_KEY is None: 
        raise RuntimeError("SECRET_KEY is not set in .env file")
    if ALGORITHM is None:
        raise RuntimeError("ALGORITHM is not set in the .env file")
    if ACCESS_TOKEN_EXPIRES_MINUTES is None:
        raise RuntimeError("ACCESS_TOKEN_EXPIRES_MINUTES is not set in the .env file")
    if ROLE_ADMIN is None:
        raise RuntimeError("ROLE_ADMIN is not set in .env file")
    
    if ROLE_USER is None:
        raise RuntimeError("ROLE_USER is not set in .env file")
    
settings = Settings()