import os
from pinecone import Pinecone, ServerlessSpec

_pc = None
_index = None

def get_pinecone_client() -> Pinecone:
    global _pc
    if _pc is None:
        api_key = os.environ.get("PINECONE_API_KEY")
        if not api_key:
            raise ValueError(
                "PINECONE_API_KEY environment variable is not set. "
                "Please configure it in your .env file."
            )
        _pc = Pinecone(api_key=api_key)
    return _pc

def get_pinecone_index(index_name: str = "youtube-rag"):
    global _index
    if _index is None:
        pc = get_pinecone_client()
        existing_indexes = pc.list_indexes().names()
        if index_name not in existing_indexes:
            pc.create_index(
                name=index_name,
                dimension=1024,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
        _index = pc.Index(index_name)
    return _index

class _LazyIndexProxy:
    def __getattr__(self, name):
        return getattr(get_pinecone_index(), name)

index = _LazyIndexProxy()