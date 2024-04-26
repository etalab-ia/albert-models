from pydantic import BaseModel
from typing import List

class ModelData(BaseModel):
    id: str
    object: str
    owned_by: str
    type: str

class GetModels(BaseModel):
    object: str
    data: List[ModelData]