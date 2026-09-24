from langchain_pinecone import PineconeVectorStore
from app.components.pinecone import get_pinecone_index
from app.components.models import embedding_model

_vector_store = None

def get_vector_store() -> PineconeVectorStore:
    global _vector_store
    if _vector_store is None:
        index = get_pinecone_index()
        _vector_store = PineconeVectorStore(index=index, embedding=embedding_model)
    return _vector_store

class _LazyVectorStoreProxy:
    def __getattr__(self, name):
        return getattr(get_vector_store(), name)

vector_store = _LazyVectorStoreProxy()