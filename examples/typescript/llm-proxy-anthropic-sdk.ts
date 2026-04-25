import Anthropic from "@anthropic-ai/sdk";

async function main() {
  const defaultHeaders: Record<string, string> = {
    Authorization: `Bearer ${process.env.MESHAGENT_ACCESS_TOKEN!}`,
  };
  if (process.env.MESHAGENT_PROJECT_ID) {
    defaultHeaders["Meshagent-Project-Id"] = process.env.MESHAGENT_PROJECT_ID;
  }

  const client = new Anthropic({
    baseURL:
      process.env.MESHAGENT_ANTHROPIC_BASE_URL ??
      "https://api.meshagent.com/anthropic",
    apiKey: "meshagent",
    defaultHeaders,
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
