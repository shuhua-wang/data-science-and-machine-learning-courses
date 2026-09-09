FROM python:3.14.7-slim-trixie

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y bash git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.12.11 /uv /uvx /usr/local/bin/
