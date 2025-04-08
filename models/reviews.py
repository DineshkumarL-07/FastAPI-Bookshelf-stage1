from pydantic import BaseModel

class Review(BaseModel):
    content: str
    rating: int