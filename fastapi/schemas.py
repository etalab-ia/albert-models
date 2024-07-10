from typing import List, Literal, Any

from pydantic import BaseModel
from openai.types import Model

class CustomModel(Model):
    type: Literal["text-generation", "text-embeddings-inference"]  # Huggingface tags


class Models(BaseModel):
    object: str
    data: List[CustomModel]


class FreeFormJSON(BaseModel):
    Any
