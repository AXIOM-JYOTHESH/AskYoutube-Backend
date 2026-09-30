from pydantic import BaseModel

class QueryRequest(BaseModel):
    url: list[str] | str
    question: str

class URLInclude(BaseModel):
    url: str