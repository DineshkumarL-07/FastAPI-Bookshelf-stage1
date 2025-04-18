from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    isbn: str
    publisher: str
    year_published: int
    copies_available: int
