FROM python:3.13-slim-bookworm

ARG MESHAGENT_VERSION="0.0.37"

ENV PIP_NO_CACHE_DIR=1

WORKDIR  /src

COPY . /src

RUN python3 -m venv .venv
ENV PATH="/src/.venv/bin:$PATH"
RUN pip3 install meshagent[all]==${MESHAGENT_VERSION}

ENTRYPOINT [ "python3", "main.py" ]
