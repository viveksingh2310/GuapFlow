from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import argon2

# Import your own modules
import database_models
import schemas

# --- 1. Password Hashing ---
# We use bcrypt as the hashing algorithm
pwd_context = CryptContext(schemes=["argon2","bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain-text password."""
    return pwd_context.hash(password)

# --- 2. JWT (Token) Configuration ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# NEVER hardcode this in production. Load from environment variables.
SECRET_KEY = "your-super-secret-key-for-this-project"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a new JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# --- 3. Authentication Dependencies ---

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(database_models.get_db) # Use your new get_db
) -> database_models.User:
    """
    Dependency to get the current logged-in user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = db.query(database_models.User).filter(database_models.User.username == token_data.username).first()
    
    if user is None:
        raise credentials_exception
        
    return user

def get_current_admin_user(
    current_user: database_models.User = Depends(get_current_user)
):
    """
    Chained dependency to verify the current user is an admin.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource."
        )
    return current_user