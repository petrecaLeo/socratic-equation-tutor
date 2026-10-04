import pytest

from evals.dataset import load_dataset
from evals.judge_prompt import build_judge_prompt, parse_verdict


def test_prompt_has_the_case_and_the_fixed_spec():
    case = next(c for c in load_dataset() if c.id == "troca-de-equacao")
    prompt = build_judge_prompt(case, "Bora! O que você faz com o − 8?")
    assert "2x − 8 = 10 (resposta certa: x = 9)" in prompt
    assert "Problema: Lucas comprou 3 cadernos" in prompt
    assert "não desconte nota por eles" in prompt
    assert "Estudante: beleza mas e essa outra aqui? 2x - 8 = 10" in prompt
    assert "Tutor: Isso! Agora falta pouco" in prompt
    assert "<idioma_pedido>português do Brasil</idioma_pedido>" in prompt
    assert "Nunca revelar a resposta final" in prompt
    assert "{" not in prompt.split("Responda só com")[0]


def test_english_case_asks_for_english():
    case = next(c for c in load_dataset() if c.language == "en")
    assert "<idioma_pedido>inglês</idioma_pedido>" in build_judge_prompt(case, "Hi")


def test_parse_verdict():
    assert parse_verdict({"reasoning": "ok", "score": 8}) == (8, "ok")


@pytest.mark.parametrize("data", [{}, [], {"score": 8}, {"reasoning": "x", "score": 0}, {"reasoning": "x", "score": 11}, {"reasoning": "x", "score": "9"}, {"reasoning": "x", "score": True}])
def test_parse_verdict_rejects(data):
    with pytest.raises(ValueError):
        parse_verdict(data)
