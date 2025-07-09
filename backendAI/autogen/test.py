import asyncio
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_core.models import UserMessage

ollama_client = OllamaChatCompletionClient(
    model="llama3.2:latest",
)

async def main():
    result = await ollama_client.create([
        UserMessage(content="What is the capital of France?", source="user")
    ])  # type: ignore
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
