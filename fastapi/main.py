import requests
import time

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from typing import Optional, Union

from schemas import CustomModel, Models

app = FastAPI(title="vLLMembeddings", version="1.0.1")

VLLM_URL = "http://vllm:8000"
TEI_URL = "http://tei:80"


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
        if model not in [vllm_model_data["id"], tei_model_data["id"]]:
            raise HTTPException(status_code=404, detail="Model not found")

        if model == vllm_model_data["id"]:
            return vllm_model_data
        else:
            return tei_model_data

    response = {"object": "list", "data": [vllm_model_data, tei_model_data]}

    return response
