import argparse
import logging
import openai
import urllib

parser = argparse.ArgumentParser(description="Test the response of a LLM model.")  # fmt: off
parser.add_argument("--base-url", type=str, default="http://localhost:8080/v1", help="Base URL of the API")  # fmt: off
parser.add_argument("--api-key", type=str, default="EMPTY", help="API key")  # fmt: off
parser.add_argument("--debug", action="store_true", help="Print debug logs")  # fmt: off

if __name__ == "__main__":

    args = parser.parse_args()
    client = openai.Client(api_key=args.api_key, base_url=args.base_url)
    level = "DEBUG" if args.debug else "INFO"
    logging.basicConfig(format="%(asctime)s:%(levelname)s: %(message)s", level=logging.getLevelName(level)) # fmt: off 
    logger = logging.getLogger(__name__)
    input = "Hello, world!"

    # /models endpoint
    try:
        logger.info(f"test: {args.base_url}/models")
        response = client.models.list()
        logger.debug(f"response of {args.base_url}/models:\n{response}")
    except Exception as e:
        logger.error(f"Failed to test {args.base_url}/models: {e}")

    # /models/{model} endpoint
    try:
        model_id = response.data[0].id
        model_id_encoded =  urllib.parse.quote(urllib.parse.quote(model_id, safe=""), safe="")
        logger.info(f"test: {args.base_url}/models/{model_id_encoded}")
        response = client.models.retrieve(model_id_encoded)
        logger.debug(f"response of {args.base_url}/models/{model_id_encoded}:\n{response}")
    except Exception as e:
        logger.error(e)

    # /chat/completions endpoint (unstreamed)
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": input}],
            stream=False,
        )
        logger.debug(f"response of {args.base_url}/chat/completions (unstreamed):\n{response}")
    except Exception as e:
        logger.error(e)

    # /chat/completions endpoint (streamed)
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": input}],
            stream=True,
        )
        logger.debug(f"response of {args.base_url}/chat/completions (unstreamed):\n{response}")
    except Exception as e:
        logger.error(e)

    # /completions endpoint (streamed)
    try:
        response = client.completions.create(
            model=model_id,
            prompt=input,
            stream=True,
        )
        logger.debug(f"response of {args.base_url}/chat/completions (streamed):\n{response}")
    except Exception as e:
        logger.error(e)

    # /completions endpoint (unstreamed)
    try:
        response = client.completions.create(
            model=model_id,
            prompt=input,
            stream=False,
        )
        logger.debug(f"response of {args.base_url}/chat/completions (streamed):\n{response}")
    except Exception as e:
        logger.error(e)
    
    # /embeddings endpoint
    try:
        response = client.embeddings.create(input=input, model=model_id)
        logger.debug(f"response of {args.base_url}/embeddings:\n{response}")
    except Exception as e:
        logger.error(e)
