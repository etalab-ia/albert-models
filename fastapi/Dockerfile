FROM python:3.12-slim

WORKDIR /code
RUN apt-get update -y && apt-get install -y curl

ADD ./pyproject.toml ./pyproject.toml
RUN pip install --upgrade pip && pip install --no-cache-dir .
ADD . ./app
