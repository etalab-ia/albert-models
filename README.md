# VLLMEmbeddings

*🔥 News :* 
- add HF_TOKEN variable for private model on HuggingFace
- new architecture for more flexiblity !

**Deploy a full OpenAI API with VLLM.**

[VLLM](https://github.com/vllm-project/vllm) is one of the state of the art libraries for deploying a Large Language Model (LLM) and its API with better generation performance. However, VLLM does not currently support the generation of embeddings (endpoint: /v1/embeddings), although it can be used to deploy an API for LLM according to OpenAI conventions (see this [discussion](https://github.com/vllm-project/vllm/discussions/310)).

This repository makes it easy to add the `/v1/embeddings` endpoint by deploying an embedding model with [HuggingFace Text Embeddings Inference (TEI)](https://github.com/huggingface/text-embeddings-inference) and serves it all on a single port. **The aim of this repository is to have a complete API that's very light, easy to use and maintain !**

## How it works ?

![](./assets/vllmembeddings.png)

**API offer the following OpenAI endpoints:**
- `/health`
- `/v1/models`
- `/v1/chat/completions`
- `/v1/completions`
- `/v1/embeddings`

You can access the other VLLM API endpoints:

- `/vllm/health`
- `/vllm/version`

And the HuggingFace Text Embeddings Inference API endpoints :
- `/tei/decode`
- `/tei/embed`
- `/tei/health`
- `/tei/embed_app`
- `/tei/embed_sparse`
- `/tei/embeddings`
- `/tei/info`
- `/tei/metrics`
- `/tei/predict`
- `/tei/rerank`
- `/tei/tokenize`
- `/tei/vertex`

You can access the VLLM API endpoint swagger with the `/docs` endpoints. However, the endpoint provided by the embeddings model, `/v1/embeddings`, is not included in this swagger. The Swagger UI is available at (official 
documentation): https://huggingface.github.io/text-embeddings-inference/#/.

## Installation

> ❓ Why build images ? To add curl package for healthcheck (nginx wait the other containers). You can replace building images by default images of VLLM and HuggingFace Text Embeddings Inference and remove healthcheck in the [docker-compose.yml](./docker-compose.yml) file.

* First, configure a *.env* file and modify *[.env.example](./.env.example)* file in this repository. For more informations about the configuration, please refer to the [configuration section](#configuration).
  
*  Then, run the containers with Docker compose :

    ```bash
    docker compose --env-file env.example up --detach
    ```

## Configuration

| variable | values |
| --- | --- |
| EMBEDDINGS_HF_REPO_ID | HuggingFace repository ID of the embeddings model. Please refer to [HuggingFace Text Embeddings Inference](https://github.com/huggingface/text-embeddings-inference) documentation to find supported models. | 
| LLM_HF_REPO_ID | HuggingFace repository ID of the LLM model. Please refer to [VLLM](https://github.com/vllm-project/vllm) documentation to find supported models. |
| TEI_ARGS | Arguments for Text Embeddings Inference (format: --arg1 <value> --arg2 <value>). Please refer to [HuggingFace Text Embeddings Inference](https://github.com/huggingface/text-embeddings-inference) documentation for more information. |
| VLLM_ARGS | Arguments for VLLM (format: --arg1 <value> --arg2 <value>). Please refer to [VLLM](https://github.com/vllm-project/vllm) documentation for more information. |
| HF_TOKEN | HuggingFace API token for private model on HuggingFace Hub. |
| API_KEY | API key for protect your model. |

## 🦜 Lanchain integration

You can use the deployed API with Langchain to create embedding vectors for your vector store. For example: 

```python
from langchain_community.embeddings import HuggingFaceHubEmbeddings

embeddings = HuggingFaceHubEmbeddings(model=f"http://localhost:8080/tei")
```

## 🔦 Tests 

```bash
python tests.py --llm-hf-repo-id TheBloke/OpenHermes-2.5-Mistral-7B-GPTQ --embeddings-hf-repo-id intfloat/e5-small --debug
```
