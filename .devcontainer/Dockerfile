FROM python:3.14.7-slim-trixie

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y bash git curl ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.12.11 /uv /uvx /usr/local/bin/

# Install nvm and Node.js (LTS)
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV NVM_DIR=/usr/local/nvm
ENV NVM_VERSION=v0.40.7
ENV NODE_VERSION=lts/*
ENV NVM_SYMLINK_CURRENT=true
RUN mkdir -p "$NVM_DIR" && \
    curl -fsSL "https://raw.githubusercontent.com/nvm-sh/nvm/${NVM_VERSION}/install.sh" | bash && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install "$NODE_VERSION" && \
    nvm alias default "$NODE_VERSION" && \
    nvm use default && \
    nvm cache clear
ENV PATH="$NVM_DIR/current/bin:$PATH"
