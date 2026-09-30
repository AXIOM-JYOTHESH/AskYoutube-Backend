import os
import time
import logging
from mistralai.client import Mistral

logger = logging.getLogger(__name__)

_client = None

def get_mistral_client() -> Mistral:
    global _client
    if _client is None:
        api_key = os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY is not set. Please configure it in your .env file.")
        _client = Mistral(api_key=api_key)
    return _client

def generate_chat_completion(messages: list[dict], model: str = "open-mistral-7b", max_retries: int = 5) -> str:
    client = get_mistral_client()
    for attempt in range(max_retries):
        try:
            response = client.chat.complete(model=model, messages=messages)
            return response.choices[0].message.content
        except Exception as e:
            if ("429" in str(e) or "rate" in str(e).lower()) and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2
                logger.warning(f"Mistral rate limit encountered. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    response = client.chat.complete(model=model, messages=messages)
    return response.choices[0].message.content

def get_embeddings(texts: list[str], model: str = "mistral-embed", max_retries: int = 3) -> list[list[float]]:
    if not texts:
        return []
    client = get_mistral_client()
    all_embeddings = []
    batch_size = 16
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        for attempt in range(max_retries):
            try:
                response = client.embeddings.create(model=model, inputs=batch)
                all_embeddings.extend([item.embedding for item in response.data])
                break
            except Exception as e:
                if ("429" in str(e) or "rate" in str(e).lower()) and attempt < max_retries - 1:
                    wait_time = 2 ** attempt + 1
                    logger.warning(f"Mistral rate limit in embeddings. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise
    return all_embeddings
