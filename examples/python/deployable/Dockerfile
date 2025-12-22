FROM us-central1-docker.pkg.dev/meshagent-life/meshagent-public/python-sdk-slim:latest

WORKDIR /app

# Copy the deployable examples (starting with the simple chatbot)
COPY simple_chatbot /simple_chatbot

# Default entrypoint for the simple chatbot example
ENTRYPOINT ["python", "/simple_chatbot/simple_chatbot.py"]