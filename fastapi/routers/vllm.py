import sys

from fastapi import APIRouter, Request

sys.path.append("..")
from schemas import FreeFormJSON

router = APIRouter(prefix="/vllm", tags=["vLLM"])

@router.get("/health")
def health_check(request: Request):
    pass # for display endpoint in swagger

@router.get("/models")
def get_models(request: Request):
    pass # for display endpoint in swagger

@router.get("/version")
def version(request: Request):
    pass # for display endpoint in swagger

@router.post("/chat/completions")
def chat_completions(request: FreeFormJSON):
    pass # for display endpoint in swagger

@router.post("/completions")
def completions(request: FreeFormJSON):
    pass # for display endpoint in swagger
