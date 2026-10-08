from passlib.context import CryptContext
from jose import jwt, JWTError

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

#Development-only configuration
SECRET_KEY = "dev-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto"
)
http_bearer = HTTPBearer()

#Returns the bcrypt hash of the given plain-text password. 
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

#Returns True if plain matches the hashed password
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

#Creates a signed JWT access token.
def create_access_token(data: dict) -> str:

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode, 
        SECRET_KEY, 
        algorithm=ALGORITHM
    )

#Dependency that extracts and validates the JWT, returning the current user.
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(http_bearer),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username = payload.get("sub")

        if not isinstance(username, str) or not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.scalar(
        select(User).where(User.username == username)
    )                      
    if user is None:
        raise credentials_exception

    return user