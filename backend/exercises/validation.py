from backend.exercises.answer_leak import leak_pattern
from backend.exercises.models import Equation

MAX_COEFFICIENT = 12
MAX_CONSTANT = 100
MAX_ANSWER = 20
MAX_STORY_CHARS = 400


class InvalidExercise(ValueError):
    pass


def check_equation(equation: Equation, difficulty: str) -> None:
    a, b, c, d = equation.a, equation.b, equation.c, equation.d
    answer = equation.solution
    if answer is None:
        raise InvalidExercise(f"{equation} não tem solução inteira")
    if max(abs(a), abs(c)) > MAX_COEFFICIENT or max(abs(b), abs(d)) > MAX_CONSTANT or abs(answer) > MAX_ANSWER:
        raise InvalidExercise(f"números grandes demais: {equation}")

    if difficulty == "hard":
        if c == 0:
            raise InvalidExercise("no difícil, x precisa aparecer dos dois lados")
        return
    if c != 0:
        raise InvalidExercise("no fácil e no médio, x aparece só do lado esquerdo")
    if difficulty == "easy" and min(a, b, d, answer) <= 0:
        raise InvalidExercise("no fácil, todos os números são positivos")
    if difficulty == "medium" and min(b, d, answer) >= 0:
        raise InvalidExercise("no médio, precisa de pelo menos um número negativo")


def parse_story(data, equation: Equation) -> str:
    try:
        story = data["story"].strip()
    except (KeyError, TypeError, AttributeError) as error:
        raise InvalidExercise(f"formato inesperado: {error!r}") from error

    if not story:
        raise InvalidExercise("história vazia")
    if len(story) > MAX_STORY_CHARS:
        raise InvalidExercise("história longa demais")
    if leak_pattern(equation.solution).search(story):
        raise InvalidExercise("a história revela a resposta")
    return story
