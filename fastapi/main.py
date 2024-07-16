import requests
import urllib
import time
import os
from typing import Optional, Union, Annotated

from fastapi import FastAPI, Request, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import Response

from routers.tei import router as TeiRouter
from routers.vllm import router as VllmRouter
from schemas import CustomModel, Models, FreeFormJSON

app = FastAPI(title="Albert models", version="1.0.2")

VLLM_URL = "http://vllm:8000"
TEI_URL = "http://tei:80"


# auth
auth_scheme = HTTPBearer(scheme_name="API key")
API_KEY = os.getenv("API_KEY")

if not API_KEY:

    def check_api_key():
        pass

else:

    def check_api_key(api_key: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)]):
        if api_key.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme")
        if api_key.credentials != API_KEY:
            raise HTTPException(status_code=403, detail="Invalid API key")

        return api_key.credentials


@app.get("/health")
def health_check(request: Request, api_key: str = Security(check_api_key)) -> Response:
    """
    Health check of vLLM model and TEI embeddings.
    """
    response = requests.get(f"{VLLM_URL}/health")
    vllm_status = response.status_code

    response = requests.get(f"{TEI_URL}/health")
    tei_status = response.status_code

    if vllm_status == 200 and tei_status == 200:
        return Response(status_code=200)
    else:
        return Response(status_code=500)


@app.get("/v1/models/{model}", tags=["OpenAI"])
@app.get("/v1/models", tags=["OpenAI"])
def get_models(
    request: Request, model: Optional[str] = None, api_key: str = Security(check_api_key)
) -> Union[Models, CustomModel]:
    """
    Show available models
    """
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else None
    vllm_model = requests.get(f"{VLLM_URL}/v1/models", headers=headers).json()
    tei_model = requests.get(f"{TEI_URL}/info", headers=headers).json()

    vllm_model_data = {
        "id": vllm_model["data"][0]["id"],
        "object": "model",
        "owned_by": "vllm",
        "created": vllm_model["data"][0]["created"],
        "type": "text-generation",
    }
    tei_model_data = {
        "id": tei_model["model_id"],
        "object": "model",
        "owned_by": "tei",
        "created": round(time.time()),
        "type": "text-embeddings-inference",
    }

    if model is not None:
        # support double encoding for model ID with "/" character
        model = urllib.parse.unquote(urllib.parse.unquote(model))
        if model not in [vllm_model_data["id"], tei_model_data["id"]]:
            raise HTTPException(status_code=404, detail="Model not found")

        if model == vllm_model_data["id"]:
            return vllm_model_data
        else:
            return tei_model_data

    response = {"object": "list", "data": [vllm_model_data, tei_model_data]}

    return response


@app.post("/v1/embeddings", tags=["OpenAI"])
def embeddings(request: FreeFormJSON):
    pass


@app.post("/v1/completions", tags=["OpenAI"])
def completions(request: FreeFormJSON):
    pass


@app.post("/v1/chat/completions", tags=["OpenAI"])
def chat_completions(request: FreeFormJSON):
    pass

# routers
app.include_router(VllmRouter)
app.include_router(TeiRouter)
