from itertools import chain

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.exercises.signing import trusted
from backend.schemas import ChatRequest
from backend.stream_events import as_events
from backend.tutor import stream_tutor

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest) -> StreamingResponse:
    messages = [message.model_dump() for message in request.messages]
    exercise = trusted(request.exercise.to_domain(), request.exercise.signature) if request.exercise else None
    chunks = stream_tutor(messages, request.language, exercise)
    # Puxar o primeiro pedaço antes de responder faz erros de chave ou de conexão
    # caírem no errors.py e virarem um JSON com o status certo.
    first = next(chunks, "")
    return StreamingResponse(as_events(chain([first], chunks)), media_type="application/x-ndjson")
