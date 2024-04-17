# VLLMEmbeddings

**Deploy a full OpenAI API with VLLM.**

[VLLM](https://github.com/vllm-project/vllm) is one of the state of the art libraries for deploying a Large Language Model (LLM) and its API with better generation performance. 

However, VLLM does not currently support the generation of embeddings (endpoint: /v1/embeddings), although it can be used to deploy an API according to OpenAI conventions.

This repository makes it easy to add the `/v1/embeddings` endpoint by deploying an embedding model with [HuggingFace Text Embeddings Inference](https://github.com/huggingface/text-embeddings-inference) and serves it all on a single port.

**API offer the following endpoints:**
- `/health`
- `/v1/models`
- `/v1/chat/completions`
- `/v1/completions`
- `/v1/embeddings`

You can access the VLLM API endpoint swagger with the `/docs` endpoints. However, the endpoint provided by the embeddings model, `/v1/embeddings`, is not included in this swagger.

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
| VLLM_HF_REPO_ID | HuggingFace repository ID of the LLM model. Please refer to [VLLM](https://github.com/vllm-project/vllm) documentation to find supported models. |
| TEXT_EMBEDDINGS_INFERENCE_IMAGE_TAG | To run embeddings model on CPU only or a specific GPU architecture, you can change image tag. Please refer to [HuggingFace Text Embeddings Inference](https://github.com/huggingface/text-embeddings-inference) documentation. To run embeddings model without GPU, you have to remove deploy section in the [docker-compose.yml](./docker-compose.yml) file for text-embeddings-inference service.|
| TEXT_EMBEDDINGS_INFERENCE_ARGS | Arguments for Text Embeddings Inference (format: --arg1 <value> --arg2 <value>). Please refer to [HuggingFace Text Embeddings Inference](https://github.com/huggingface/text-embeddings-inference) documentation for more information. |
| VLLM_ARGS | Arguments for VLLM (format: --arg1 <value> --arg2 <value>). Please refer to [VLLM](https://github.com/vllm-project/vllm) documentation for more information. |
