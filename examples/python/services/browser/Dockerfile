FROM python:3.13-slim-bookworm

ARG MESHAGENT_VERSION="0.0.23"

ENV PIP_NO_CACHE_DIR=1

WORKDIR  /src

COPY . /src

RUN python3 -m venv .venv
ENV PATH="/src/.venv/bin:$PATH"
RUN pip3 install meshagent-api==${MESHAGENT_VERSION}   \
                 meshagent-agents==${MESHAGENT_VERSION} \
                 meshagent-tools==${MESHAGENT_VERSION} \
                 meshagent-computers==${MESHAGENT_VERSION}

ENTRYPOINT [ "python3", "main.py" ]