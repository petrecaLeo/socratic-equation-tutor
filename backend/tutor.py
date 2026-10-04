from collections.abc import Iterator

from anthropic.types import MessageParam

from backend.config import MAX_HISTORY_MESSAGES, TUTOR_MAX_TOKENS, TUTOR_MODEL
from backend.exercises.models import Exercise
from backend.llm import client, log_cost, reply_text
from backend.prompts.tutor import ACTIVE_VERSION, build_tutor_system


def tutor_params(messages: list[MessageParam], system: str) -> dict:
    return {
        "model": TUTOR_MODEL,
        "max_tokens": TUTOR_MAX_TOKENS,
        "system": system,
        "messages": messages,
        # Sem raciocínio prévio: equação do 1º grau não precisa, e pensamento é cobrado como saída.
        "thinking": {"type": "between_tools"},
        # O Sonnet 5.5 recusa temperature (erro 400); o ajuste disponível é o effort.
        "output_config": {"effort": "low"},
    }


def recent_messages(messages: list[MessageParam], limit: int = MAX_HISTORY_MESSAGES) -> list[MessageParam]:
    window = messages[-limit:]
    # Começa sempre por uma fala do aluno, para o tutor não ver uma resposta sem a pergunta.
    while window and window[0]["role"] != "user":
        window = window[1:]
    return window


def request_params(
    messages: list[MessageParam], language: str, exercise: Exercise | None, version: str = ACTIVE_VERSION
) -> dict:
    return tutor_params(recent_messages(messages), build_tutor_system(language, exercise, version))


def ask_tutor(
    messages: list[MessageParam], language: str, exercise: Exercise | None = None, version: str = ACTIVE_VERSION
) -> str:
    response = client.messages.create(**request_params(messages, language, exercise, version))
    log_cost("tutor", TUTOR_MODEL, response)
    return reply_text(response)


def stream_tutor(messages: list[MessageParam], language: str, exercise: Exercise | None = None) -> Iterator[str]:
    with client.messages.stream(**request_params(messages, language, exercise)) as stream:
        yield from stream.text_stream
        response = stream.get_final_message()
    log_cost("tutor", TUTOR_MODEL, response)
