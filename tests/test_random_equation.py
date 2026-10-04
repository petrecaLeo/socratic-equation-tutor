import random

import pytest

from backend.exercises.random_equation import random_equation
from backend.exercises.validation import check_equation


@pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
def test_every_draw_is_valid_and_varied(difficulty):
    rng = random.Random(42)
    equations = [random_equation(difficulty, rng=rng) for _ in range(300)]
    for equation in equations:
        check_equation(equation, difficulty)
    assert len({str(e) for e in equations}) > 150


def test_avoids_recent_equations():
    rng = random.Random(7)
    first = random_equation("easy", rng=rng)
    for _ in range(50):
        assert random_equation("easy", {str(first)}, rng=rng) != first
