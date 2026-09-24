import os
from mistralai.client import Mistral

_client = None

def get_mistral_client() -> Mistral:
    global _client
    if _client is None:
        api_key = os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY is not set. Please configure it in your .env file.")
        _client = Mistral(api_key=api_key)
    return _client

def generate_chat_completion(messages: list[dict], model: str = "mistral-small-2506") -> str:
    client = get_mistral_client()
    response = client.chat.complete(model=model, messages=messages)
    return response.choices[0].message.content

def get_embeddings(texts: list[str], model: str = "mistral-embed") -> list[list[float]]:
    client = get_mistral_client()
    response = client.embeddings.create(model=model, inputs=texts)
    return [item.embedding for item in response.data]