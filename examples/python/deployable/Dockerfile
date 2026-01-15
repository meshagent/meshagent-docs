ARG MESHAGENT_SDK_IMAGE="meshagent/python-sdk:latest" 

FROM ${MESHAGENT_SDK_IMAGE}

# Copy the deployable examples 
RUN python3 -m pip install --no-cache-dir httpx 
WORKDIR /src
COPY . /src
