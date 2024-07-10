import sys

from fastapi import APIRouter, Request

sys.path.append("..")
from schemas import FreeFormJSON

router = APIRouter(prefix="/tei", tags=["Text Embeddings Inference"])

@router.post("/decode")
def decode(request: FreeFormJSON):
    pass # for display endpoint in swagger

@router.post("/embed")
def embeddings(request: FreeFormJSON):
    pass # for display endpoint in swagger

@router.post("/embed_all")
def embeddings_all(request: FreeFormJSON):
    pass # for display endpoint in swagger

@router.post("/embed_sparse")
def embeddings_sparse(request: FreeFormJSON):
    pass # for display endpoint in swagger

@router.get("/health")
def health_check(request: Request):
    pass # for display endpoint in swagger

@router.get("/info")
def info(request: Request):
    pass # for display endpoint in swagger

@router.get("/metrics")
def metrics(request: Request):
    pass # for display endpoint in swagger

@router.post("/predict")
def predict(request: FreeFormJSON):
    pass # for display endpoint in swagger

@router.post("/rerank")
def rerank(request: FreeFormJSON):
    pass # for display endpoint in swagger

@router.post("/similarity")
def similarity(request: FreeFormJSON):
    pass # for display endpoint in swagger

@router.post("/tokenize")
def tokenize(request: FreeFormJSON):
    pass # for display endpoint in swagger

@router.post("/v1/embeddings")
def embeddings(request: FreeFormJSON):
    pass # for display endpoint in swagger