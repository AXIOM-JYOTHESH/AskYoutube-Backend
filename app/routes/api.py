from fastapi import APIRouter, Query
from app.models.schemas import QueryRequest, URLInclude
from app.services.youtube import process_query, loadURL

router = APIRouter(prefix="/api")

@router.post('/load')
def load_video(data: URLInclude):
    response = loadURL(data.url)
    return {
        "success": response == "Transcripts Available",
        "message": response,
    }


@router.post("/ask")
def ask_question(data: QueryRequest):
    response = process_query(data.url, data.question)
    return {
        "success": response != "NA",
        "message": response,
    }


@router.get("/ask")
def ask_question_query(
    question: str = Query(..., description="The question to ask about the video"),
    url: list[str] = Query(..., description="YouTube video URL(s)"),
):
    response = process_query(url, question)
    return {
        "success": response != "NA",
        "message": response,
    }