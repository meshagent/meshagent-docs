// npx tsx llm-proxy-anthropic-sdk.ts

import Anthropic from "@anthropic-ai/sdk";

async function main() {
  const client = new Anthropic({
    baseURL: process.env.ANTHROPIC_BASE_URL!,
    apiKey: process.env.ANTHROPIC_API_KEY!,
    defaultHeaders: {
      "Meshagent-Project-Id": process.env.MESHAGENT_PROJECT_ID!,
    },
  });

  const message = await client.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 512,
    messages: [
      {
        role: "user",
        content: "Tell me a fun fact about AI.",
      },
    ],
  });

  console.log(message.content[0]);
}

void main();
