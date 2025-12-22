ARG MESHAGENT_SDK_IMAGE="meshagent/python-sdk-slim:latest"

FROM ${MESHAGENT_SDK_IMAGE}

# Copy the deployable examples (starting with the simple chatbot)
COPY . /src

WORKDIR /src

# Default entrypoint for the simple chatbot example
ENTRYPOINT ["python", "/simple_chatbot/simple_chatbot.py"]