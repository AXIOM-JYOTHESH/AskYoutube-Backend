from pinecone import Pinecone, ServerlessSpec
import os

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
if "youtube-rag" not in pc.list_indexes().names():
    pc.create_index(
        name="youtube-rag",
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
index = pc.Index("youtube-rag")