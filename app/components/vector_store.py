from app.components.pinecone import get_pinecone_index
from app.components.models import get_embeddings

def add_documents_to_pinecone(texts: list[str], video_id: str, batch_size: int = 100):
    if not texts:
        return
    embeddings = get_embeddings(texts)
    index = get_pinecone_index()
    vectors = [
        {
            "id": f"{video_id}_{i}",
            "values": emb,
            "metadata": {
                "video_id": video_id,
                "text": text,
            },
        }
        for i, (text, emb) in enumerate(zip(texts, embeddings))
    ]
    for i in range(0, len(vectors), batch_size):
        index.upsert(vectors=vectors[i:i + batch_size])

def query_pinecone(queries: list[str], video_ids: list[str], top_k: int = 10) -> list[str]:
    if not queries or not video_ids:
        return []
    embeddings = get_embeddings(queries)
    index = get_pinecone_index()
    retrieved_texts: list[str] = []
    seen = set()

    for emb in embeddings:
        res = index.query(
            vector=emb,
            filter={"video_id": {"$in": video_ids}},
            top_k=top_k,
            include_metadata=True,
        )
        matches = getattr(res, "matches", []) or (res.get("matches", []) if isinstance(res, dict) else [])
        for m in matches:
            metadata = getattr(m, "metadata", None) or (m.get("metadata") if isinstance(m, dict) else None)
            if metadata and "text" in metadata:
                text = metadata["text"]
                if text not in seen:
                    seen.add(text)
                    retrieved_texts.append(text)
    return retrieved_texts
