from pydantic import BaseModel, Field
from typing import Optional

class CreateCategory(BaseModel):
    name: str = Field(..., examples=["Fiction"])

class ReadCategory(BaseModel):
    id: str = Field(..., examples=["6769be7156ca61f944fa3f90"])
    name: str = Field(..., examples=['Fiction'])

class UpdateCategory(BaseModel):
    name: Optional[str] = Field(None, examples=['Fiction'])
    