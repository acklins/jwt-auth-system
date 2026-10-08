from pydantic import BaseModel, ConfigDict, Field

#Schema for user registration.
class UserCreate(BaseModel):

    username: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=200)
    password: str = Field(min_length=8)

#Schema for returning user data (no password fields)
class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)

#Schema for the JWT response.
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
