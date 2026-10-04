import re

import pytest

from backend.exercises.models import Equation, Exercise
from backend.prompts.tutor import EXAMPLE_EQUATION, TUTOR_PROMPTS, build_tutor_system
from evals.dataset import load_dataset

EXERCISE = Exercise("Ana comprou 2 cadernos.", Equation(2, 3, 0, 11))


@pytest.mark.parametrize("version", list(TUTOR_PROMPTS))
def test_every_version_fills_all_placeholders(version):
    prompt = build_tutor_system("en", EXERCISE, version)
    assert "Equação: 2x + 3 = 11" in prompt
    assert "x = 4" in prompt
    assert "inglês" in prompt
    assert "{" not in prompt and "}" not in prompt


def test_v2_puts_the_exercise_inside_its_tag():
    prompt = build_tutor_system("pt", EXERCISE, "v2")
    assert "<exercicio>\nProblema: Ana comprou 2 cadernos." in prompt
    assert "Responda sempre em português do Brasil" in prompt


@pytest.mark.parametrize("version", [v for v, prompt in TUTOR_PROMPTS.items() if "<exemplos>" in prompt])
def test_examples_do_not_use_answers_from_the_dataset(version):
    # Exemplo é copiado ao pé da letra: a resposta dele não pode ser a de nenhum caso.
    examples = TUTOR_PROMPTS[version].split("<exemplos>")[1]
    example_answers = {int(n) for n in re.findall(r"x = (-?\d+)", examples)}
    assert example_answers
    assert not example_answers & {case.answer for case in load_dataset()}


@pytest.mark.parametrize("version", [v for v, prompt in TUTOR_PROMPTS.items() if "<exemplos>" in prompt])
def test_example_equation_constant_matches_the_prompts(version):
    # Se os exemplos mudarem, o EXAMPLE_EQUATION (que o gerador evita) precisa mudar junto.
    assert f"<equacao>{EXAMPLE_EQUATION}</equacao>" in TUTOR_PROMPTS[version]
