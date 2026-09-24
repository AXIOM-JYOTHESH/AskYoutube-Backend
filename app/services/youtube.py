import logging
from youtube_transcript_api import YouTubeTranscriptApiException
from app.db.config import collection
from app.components.prompt import format_prompt
from app.components.youtube_transcripts_loader import loader
from app.components.models import generate_chat_completion
from app.components.vector_store import add_documents_to_pinecone, query_pinecone
from app.components.textsplitter import text_splitter
from app.components.utils import get_video_id

logger = logging.getLogger(__name__)

def generate_multi_queries(question: str) -> list[str]:
    """Generate multiple query variations using Mistral to improve retrieval recall."""
    try:
        prompt = (
            "You are an AI assistant helping with search. "
            "Generate 3 different search queries to find relevant sections in a video transcript for the user question. "
            "Provide each query on a new line. Do NOT include numbers or bullet points.\n\n"
            f"User question: {question}"
        )
        content = generate_chat_completion([{"role": "user", "content": prompt}])
        queries = [q.strip() for q in content.strip().split("\n") if q.strip()]
        return [question] + queries[:3]
    except Exception as e:
        logger.warning(f"Multi-query generation failed: {e}. Falling back to original question.")
        return [question]

def process_query(url: list[str], question: str) -> str:
    video_ids = []
    for l in url:
        v = get_video_id(l)
        if v:
            video_ids.append(v)
    if not video_ids:
        return "NA"

    try:
        queries = generate_multi_queries(question)
        retrieved_texts = query_pinecone(queries, video_ids, top_k=5)
        context = "\n\n".join(retrieved_texts)

        prompt = format_prompt(context=context, query=question)
        response = generate_chat_completion([{"role": "user", "content": prompt}])
        return response
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return "NA"

def loadURL(url: str) -> str:
    video_id = get_video_id(url)
    if not video_id:
        return "Invalid YouTube URL"

    vid = collection.find_one({"video_id": video_id})
    if vid:
        return "Transcripts Available" if vid.get("processable") else "No Captions Available for this video"

    try:
        transcripts = loader.fetch(video_id=video_id, languages=["en", "hi", "gu"])
        transcript = " ".join([x.text for x in transcripts])
        texts = text_splitter.split_text(transcript)

        add_documents_to_pinecone(texts=texts, video_id=video_id)
        print("Inserted into Pinecone")

        collection.insert_one({
            "video_id": video_id,
            "processable": True,
        })
        return "Transcripts Available"
    except YouTubeTranscriptApiException:
        collection.insert_one({
            "video_id": video_id,
            "processable": False,
        })
        return "No Captions Available for this video"