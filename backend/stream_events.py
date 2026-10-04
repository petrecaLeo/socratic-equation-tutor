import json
from collections.abc import Iterator

import anthropic


def event(kind: str, **data) -> str:
    return json.dumps({"type": kind, **data}, ensure_ascii=False) + "\n"


def as_events(chunks: Iterator[str]) -> Iterator[str]:
    try:
        for text in chunks:
            if text:
                yield event("text", text=text)
    except anthropic.APIError as error:
        # O status 200 já foi enviado: o erro vai como evento, para o front saber que a resposta ficou pela metade.
        print(f"[erro] stream interrompido: {error!r}")
        yield event("error", code="stream_interrupted")
        return
    yield event("done")
