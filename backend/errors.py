import anthropic
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from backend.exercises.generator import ExerciseGenerationFailed


# O back devolve só um código; o texto, no idioma da pessoa, fica com o front.
def error_response(code: str, status_code: int) -> JSONResponse:
    return JSONResponse({"code": code}, status_code=status_code)


def register_error_handlers(app: FastAPI) -> None:
    # Sem detalhes: a resposta padrão do FastAPI devolve o dado enviado e o formato interno dos schemas.
    @app.exception_handler(RequestValidationError)
    async def invalid_request(request: Request, error: RequestValidationError) -> JSONResponse:
        return error_response("invalid_request", 422)

    @app.exception_handler(anthropic.AuthenticationError)
    async def invalid_api_key(request: Request, error: anthropic.AuthenticationError) -> JSONResponse:
        return error_response("invalid_api_key", 500)

    @app.exception_handler(anthropic.APIError)
    async def api_unavailable(request: Request, error: anthropic.APIError) -> JSONResponse:
        print(f"[erro] {error!r}")
        return error_response("api_unavailable", 502)

    @app.exception_handler(ExerciseGenerationFailed)
    async def exercise_failed(request: Request, error: ExerciseGenerationFailed) -> JSONResponse:
        return error_response("exercise_failed", 502)
