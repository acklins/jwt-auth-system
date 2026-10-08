from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.schemas.user import(
    UserCreate,
    UserResponse, 
    TokenResponse
) 
from app.models.user import User
from app.database import get_db

from app.auth import (
    hash_password, 
    verify_password, 
    create_access_token, 
    get_current_user
)

router = APIRouter()

#Registers a new user.
@router.post(
        "/register", 
        response_model=UserResponse, 
        status_code=status.HTTP_201_CREATED
)
def register(
    user: UserCreate, 
    db: Session = Depends(get_db)
):
    existing_username = db.scalar(
        select(User).where(User.username == user.username)
    )
    if existing_username:
        raise HTTPException(
            status_code=409,
            detail="Username already registered"
        )

    existing_email = db.scalar(
        select(User).where(User.email == user.email)
    )
    if existing_email:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#  Authenticates user credentials and returns a JWT access token.
@router.post("/token", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = db.scalar(
        select(User).where(
            User.username == form_data.username
        )
    )
    if user is None or not verify_password(
        form_data.password, 
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        {"sub": user.username}
    )
    return TokenResponse(
        access_token=access_token, 
        token_type="bearer"
        
    )

#Returns the currently authenticated user.
@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user

#Additonal protected endpoint (GET /dashboard)
@router.get("/dashboard")
def get_dashboard(current_user=Depends(get_current_user)):
    return {
        "message": f"Welcome to your dashboard, {current_user.username}!",
        "user_id": current_user.id,
        "authenticated": True
    }
