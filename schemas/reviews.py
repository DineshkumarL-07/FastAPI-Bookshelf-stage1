from typing import Optional
from pydantic import Field, BaseModel

class CreateReview(BaseModel):
    content: str = Field(..., examples=["A captivating story with deep symbolism."])
    rating: int = Field(..., examples=[5])

class ReadReview(BaseModel):
    id: str = Field(..., examples=["9876fd7156ca61f944fa3f91"])
    content: str = Field(..., examples=["A captivating story with deep symbolism."])
    rating: int = Field(..., examples=[5])
    book_id: str = Field(..., examples=["6769be7156ca61f944fa3f90"])

class UpdateReview(BaseModel):

    content: Optional[str] = Field(None, examples=["A captivating story with deep symbolism."])
    rating: Optional[int] = Field(None, examples=[5])