import pytest

from backend.exercises.models import Equation


@pytest.mark.parametrize(
    ("equation", "solution"),
    [
        (Equation(2, 3, 0, 11), 4),
        (Equation(4, -7, 0, -3), 1),
        (Equation(5, -3, 2, 9), 4),
        (Equation(-1, 4, 1, -6), 5),
        (Equation(3, 1, 0, 11), None),
        (Equation(2, 1, 2, 5), None),
    ],
)
def test_solution(equation, solution):
    assert equation.solution == solution


@pytest.mark.parametrize(
    ("equation", "text"),
    [
        (Equation(2, 3, 0, 11), "2x + 3 = 11"),
        (Equation(4, -7, 0, -3), "4x − 7 = −3"),
        (Equation(1, 0, 0, 9), "x = 9"),
        (Equation(-1, 4, 1, -6), "−x + 4 = x − 6"),
        (Equation(-12, 5, 3, 0), "−12x + 5 = 3x"),
    ],
)
def test_format(equation, text):
    assert str(equation) == text
