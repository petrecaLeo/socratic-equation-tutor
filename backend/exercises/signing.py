import hashlib
import hmac
import secrets

from backend.exercises.models import Exercise

# Chave nova toda vez que o servidor sobe: só ele consegue assinar uma história.
_KEY = secrets.token_bytes(32)


def sign(exercise: Exercise) -> str:
    equation = exercise.equation
    message = f"{exercise.story}\n{equation.a}\n{equation.b}\n{equation.c}\n{equation.d}".encode()
    return hmac.new(_KEY, message, hashlib.sha256).hexdigest()


def trusted(exercise: Exercise, signature: str | None) -> Exercise:
    """A história vai para o system prompt do tutor, então só entra se foi o servidor que a escreveu.

    Sem assinatura válida (texto editado pelo cliente, ou servidor reiniciado), a história é descartada.
    A equação fica, porque são só números já validados.
    """
    if not exercise.story or (signature and hmac.compare_digest(sign(exercise), signature)):
        return exercise
    print("[segurança] história sem assinatura válida: descartada")
    return Exercise("", exercise.equation)
