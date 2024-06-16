from pydantic import BaseModel
from typing import List

class Model(BaseModel):
    id: str
    object: str
    owned_by: str
    type: str

class Models(BaseModel):
    object: str
    data: List[Model]