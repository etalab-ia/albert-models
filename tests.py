import argparse
import requests
import logging

parser = argparse.ArgumentParser(description="Test the response of a LLM model.")  # fmt: off
parser.add_argument("--embeddings-hf-repo-id", type=str, required=True, help="Hugging Face model ID for embeddings")  # fmt: off
parser.add_argument("--llm-hf-repo-id", type=str, required=True, help="Hugging Face model ID for LLM")  # fmt: off
parser.add_argument("--port", type=int, default=8080, help="Model port")  # fmt: off
parser.add_argument("--host", type=str, default="localhost", help="Model host (default: localhost)")  # fmt: off
parser.add_argument("--debug", action="store_true", help="Print debug logs")  # fmt: off

# @TODO: test with API key

if __name__ == "__main__":
    args = parser.parse_args()
    input = "Hello, world!"

    level = "DEBUG" if args.debug else "INFO"
    logging.basicConfig(
        format="%(asctime)s:%(levelname)s: %(message)s",
        level=logging.getLevelName(level),
    )
    logger = logging.getLogger(__name__)

    # v1/health endpoint
    endpoint = f"http://{args.host}:{args.port}/health"
    response = requests.get(endpoint, verify=False)
    logger.info(f"Response status code: {response.status_code}")
    logger.debug(f"Response headers: {response.headers}")
    logger.debug(f"Response content: {response.content}")

    assert response.status_code == 200, "invalid response status code"

    # v1/models endpoint
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
