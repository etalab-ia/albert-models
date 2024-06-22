import argparse
import requests
import logging
import openai
import urllib

parser = argparse.ArgumentParser(description="Test the response of a LLM model.")  # fmt: off
parser.add_argument("--base-url", type=str, help="Base URL of the API")  # fmt: off
parser.add_argument("--api-key", type=str, help="API key")  # fmt: off
parser.add_argument("--debug", action="store_true", help="Print debug logs")  # fmt: off

# @TODO: test with API key
# @TODO: remove model args
# @TODO: add openai package for the tests

if __name__ == "__main__":
    args = parser.parse_args()
    client = openai.Client(api_key=args.api_key, base_url=args.base_url)
    level = "DEBUG" if args.debug else "INFO"
    logging.basicConfig(format="%(asctime)s:%(levelname)s: %(message)s", level=logging.getLevelName(level)) # fmt: off 
    logger = logging.getLogger(__name__)

    # health endpoint
    logger.info(f"test: {args.base_url}/health")
    response = requests.get(f"{args.base_url}/health", verify=False)
    assert response.status_code == 200, f"invalid response status code of {args.base_url}/health"
    logger.debug(f"response status code of {args.base_url}/health: {response.status_code}")

    # /models endpoint
    logger.info(f"test: {args.base_url}/models")
    response = client.models.list()
    logger.debug(f"response of {args.base_url}/models:\n{response}")

    # /models/{model} endpoint
    model_id = response.data[0].id
    model_id_encoded = urllib.parse.quote(model_id)
    logger.info(f"test: {args.base_url}/models/{model_id_encoded}")
    response = client.models.retrieve(model_id_encoded)
    logger.debug(f"response of {args.base_url}/models/{model_id_encoded}:\n{response}")

    # /chat/completions endpoint (unstreamed)
    response = client.chat.create(
        model=model_id,
        messages=[{"role": "user", "content": "Hello, world!"}],
        stream=False,
    )
    logger.debug(f"response of {args.base_url}/chat/completions (unstreamed):\n{response}")

    # /chat/completions endpoint (streamed)
    response = client.chat.create(
        model=model_id,
        messages=[{"role": "user", "content": "Hello, world!"}],
        stream=True,
    )
    logger.debug(f"response of {args.base_url}/chat/completions (streamed):\n{response}")

    input = "Hello, world!"



    # /v1/models endpoint


    endpoint = f"http://{args.host}:{args.port}/v1/models"
    response = requests.get(endpoint, verify=False)

    logger.info(f"Response status code: {response.status_code}")
    logger.debug(f"Response headers: {response.headers}")
    logger.debug(f"Response content: {response.content}")

    assert response.status_code == 200, "invalid response status code"

    # v1/embeddings endpoint
    endpoint = f"http://{args.host}:{args.port}/v1/embeddings"
    data = {"input": input, "model": args.embeddings_hf_repo_id, "user": "test"}

    response = requests.post(endpoint, json=data, verify=False)
    logger.info(f"Response status code: {response.status_code}")
    logger.debug(f"Response headers: {response.headers}")
    logger.debug(f"Response content: {response.content}")

    assert response.status_code == 200, "invalid response status code"

    # v1/chat/completions endpoint
    endpoint = f"http://{args.host}:{args.port}/v1/chat/completions"
    data = {
        "model": args.llm_hf_repo_id,
        "messages": [{"role": "user", "content": input}],
        "stream": False,
        "user": "test",
    }
    response = requests.post(endpoint, json=data, verify=False)
    logger.info(f"Response status code: {response.status_code}")
    logger.debug(f"Response headers: {response.headers}")
    logger.debug(f"Response content: {response.content}")

    assert response.status_code == 200, "invalid response status code"
