import requests
import time

from fastapi import FastAPI, Request
from fastapi.responses import Response
from typing import Optional, Union

from schemas import CustomModel, Models

app = FastAPI(title="VLLMEmbeddings", version="0.0.1")

VLLM_URL = f"http://vllm:8000"
TEI_URL = f"http://tei:80"


@app.get("/health")
def health_check(request: Request) -> Response:
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


@app.get("/v1/models")
def get_models(request: Request, model: Optional[str] = None) -> Union[Models, CustomModel]:
    """
    Show available models
    """

    vllm_model = requests.get(f"{VLLM_URL}/v1/models").json()
    tei_model = requests.get(f"{TEI_URL}/info").json()

    response = {
        "object": "list",
        "data": [
            {
                "id": vllm_model["data"][0]["id"],
                "object": "model",
                "owned_by": "vllm",
                "created": vllm_model["data"][0]["created"],
                "type": "text-generation",
            },
            {
                "id": tei_model["model_id"],
                "object": "model",
                "owned_by": "tei",
                "created": round(time.time()),
                "type": "text-embeddings-inference",
            },
        ],
    }

    return response
