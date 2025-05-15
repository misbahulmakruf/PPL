from fastapi import APIRouter
from pydantic import BaseModel
from api.rag_engine import get_rag_response

router = APIRouter()

class AssistantRequest(BaseModel):
    query: str

@router.post("/assistant")
def handle_assistant_query(req: AssistantRequest):
    response = get_rag_response(req.query)
    return {"response": response}
