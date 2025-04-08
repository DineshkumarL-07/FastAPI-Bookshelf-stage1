from pydantic import BaseModel, Field
from typing import Optional 

class UserCreate(BaseModel):
    username: str = Field(..., examples=["john_doe"])
    email: str = Field(..., examples=["john@example.com"])
    full_name: str = Field(..., examples=["John Doe"])
    password: str = Field(..., examples=["securepassword123"])

class UserRead(BaseModel):
    id: str = Field(..., examples=["6769be7156ca61f944fa3f90"])
    username: str = Field(..., examples=["john_doe"])
    email: str = Field(..., examples=["john@example.com"])
    full_name: str = Field(..., examples=["John Doe"])

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, examples=["john_doe"])
    email: Optional[str] = Field(None, examples=["john@example.com"])
    full_name: Optional[str] = Field(None, examples=["John Doe"])
    password: Optional[str] = Field(None, examples=["securepassword123"])
