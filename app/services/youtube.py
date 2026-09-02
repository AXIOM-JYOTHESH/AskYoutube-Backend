from youtube_transcript_api import YouTubeTranscriptApiException
from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableParallel
from langchain_core.documents import Document
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from app.db.config import collection
from app.components.prompt import template
from app.components.youtube_transcripts_loader import loader
from app.components.models import llm
from app.components.vector_store import vector_store
from app.components.textsplitter import text_splitter
from app.components.output_parser import parser
from app.components.utils import get_video_id, format_docs

sequence = template | llm | parser

def process_query(url: list[str], question: str):
    video_ids = list()
    for l in url:
        v = get_video_id(l)
        if v:
            video_ids.append(v)
    try:
        r = vector_store.as_retriever(search_type = 'mmr', search_kwargs={"k": 10, "lambda_mult": 0.5, "filter": {"video_id": {"$in": video_ids}}})
        retriever = MultiQueryRetriever.from_llm(retriever=r, llm=llm, include_original=True)
        parallel = RunnableParallel({
            "context": retriever | RunnableLambda(format_docs),
            "query": RunnablePassthrough()
        })
        chain = parallel | sequence

        response = chain.invoke(question)
        return response
    except Exception:
        return "NA"

def loadURL(url: str):
    video_id = get_video_id(url)
    vid = collection.find_one({"video_id": video_id})
    if vid:
        return "Transcripts Available" if vid['processable'] else "No Captions Available for this video"
    try: 
        transcripts = loader.fetch(video_id=video_id, languages=['en', 'hi', 'gu'])
        transcript = " ".join([x.text for x in transcripts])
        texts = text_splitter.split_text(transcript)
        docs = [Document(page_content=t, metadata={"video_id": video_id}) for t in texts]
        # ids = [f"{video_id}_{i}" for i in range(len(docs))]
        id=vector_store.add_documents(documents=docs)
        print("Inserted into Pinecone")
        collection.insert_one({
            "video_id": video_id,
            "processable": True
        })
        return "Transcripts Available"
    except YouTubeTranscriptApiException:
        collection.insert_one({
            "video_id": video_id,
            "processable": False
        })
        return "No Captions Available for this video"