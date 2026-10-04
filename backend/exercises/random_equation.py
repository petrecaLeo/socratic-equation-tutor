import random

from backend.exercises.models import Equation
from backend.exercises.validation import InvalidExercise, check_equation

MAX_DRAWS = 1000


def _nonzero(rng: random.Random, limit: int) -> int:
    return rng.choice([n for n in range(-limit, limit + 1) if n != 0])


def _candidate(difficulty: str, rng: random.Random) -> Equation:
    # Monta de trás para frente: escolhe a resposta e calcula o d, então a conta sempre fecha.
    # A resposta é sempre positiva, porque "quantos cadernos" com resposta negativa vira história sem sentido.
    answer = rng.randint(1, 12)
    a = rng.randint(2, 9)
    b = rng.randint(1, 30) if difficulty == "easy" else _nonzero(rng, 30)
    c = rng.randint(1, a - 1) if difficulty == "hard" else 0
    return Equation(a, b, c, a * answer + b - c * answer)


def random_equation(difficulty: str, avoid: set[str] = frozenset(), rng: random.Random | None = None) -> Equation:
    rng = rng or random.Random()
    for _ in range(MAX_DRAWS):
        equation = _candidate(difficulty, rng)
        try:
            check_equation(equation, difficulty)
        except InvalidExercise:
            continue
        if str(equation) not in avoid:
            return equation
    raise RuntimeError(f"não achei uma equação nova para a dificuldade {difficulty}")
