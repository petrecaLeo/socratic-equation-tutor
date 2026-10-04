import pytest

from backend.exercises.models import Equation
from backend.exercises.validation import InvalidExercise, check_equation, parse_story


@pytest.mark.parametrize(
    ("equation", "difficulty"),
    [
        (Equation(3, 5, 0, 20), "easy"),
        (Equation(4, -7, 0, -3), "medium"),
        (Equation(5, -3, 2, 9), "hard"),
    ],
)
def test_valid_equations(equation, difficulty):
    check_equation(equation, difficulty)


@pytest.mark.parametrize(
    ("equation", "difficulty"),
    [
        (Equation(3, 1, 0, 11), "easy"),     # sem solução inteira
        (Equation(30, 3, 0, 63), "easy"),    # coeficiente grande demais
        (Equation(2, 3, 0, 63), "easy"),     # resposta grande demais (x = 30)
        (Equation(3, -5, 0, 10), "easy"),    # fácil com negativo
        (Equation(3, 5, 0, 20), "medium"),   # médio sem nenhum negativo
        (Equation(3, 5, 0, 20), "hard"),     # difícil sem x dos dois lados
        (Equation(5, -3, 2, 9), "easy"),     # fácil com x dos dois lados
    ],
)
def test_invalid_equations(equation, difficulty):
    with pytest.raises(InvalidExercise):
        check_equation(equation, difficulty)


def test_parse_story():
    equation = Equation(3, 5, 0, 20)
    assert parse_story({"story": "  Lucas comprou 3 cadernos. Quanto custou cada um?  "}, equation) == "Lucas comprou 3 cadernos. Quanto custou cada um?"


@pytest.mark.parametrize(
    "data",
    [
        {},
        [],
        {"story": 3},
        {"story": "   "},
        {"story": "a" * 401},
        {"story": "Lucas pagou 20 reais, então x = 5. Quanto custou?"},
    ],
)
def test_parse_story_rejects(data):
    with pytest.raises(InvalidExercise):
        parse_story(data, Equation(3, 5, 0, 20))
