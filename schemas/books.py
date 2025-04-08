from pydantic import BaseModel, Field
from typing import Optional


class BookCreate(BaseModel):
    title: str = Field(..., examples=["The Great Gatsby"])
    author: str = Field(..., examples=["F. Scott Fitzgerald"])
    isbn: str = Field(..., examples=["1234567890123"])
    publisher: str = Field(..., examples=["Charles Scribner's Sons"])
    year_published: int = Field(..., examples=[1925])
    copies_available: int = Field(..., examples=[5])


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, examples=["The Great Gatsby"])
    author: Optional[str] = Field(None, examples=["F. Scott Fitzgerald"])
    isbn: Optional[str] = Field(None, examples=["1234567890123"])
    publisher: Optional[str] = Field(None, examples=["Charles Scribner's Sons"])
    year_published: Optional[int] = Field(None, examples=[1925])
    copies_available: Optional[int] = Field(None, examples=[5])


class BookResponse(BaseModel):
    id: str = Field(..., examples=["6769be7156ca61f944fa3f90"])
    title: str = Field(..., examples=["The Great Gatsby"])
    author: str = Field(..., examples=["F. Scott Fitzgerald"])
    isbn: str = Field(..., examples=["1234567890123"])
    publisher: str = Field(..., examples=["Charles Scribner's Sons"])
    year_published: int = Field(..., examples=[1925])
    copies_available: int = Field(..., examples=[5])
