from langchain_pinecone import PineconeVectorStore
from app.components.pinecone import index
from app.components.models import embedding_model

vector_store = PineconeVectorStore(index=index, embedding=embedding_model)