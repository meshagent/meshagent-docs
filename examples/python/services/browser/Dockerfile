ARG MESHAGENT_SDK_IMAGE="meshagent/python-sdk:latest"

FROM ${MESHAGENT_SDK_IMAGE}

ENV PIP_NO_CACHE_DIR=1

WORKDIR  /src

RUN uv pip install meshagent-agents[all]

COPY . /src

ENTRYPOINT [ "python3", "main.py" ]
