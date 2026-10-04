import pytest

from evals.checks import count_sentences, grade_by_code, is_plain_text, is_short, leak_pattern
from evals.dataset import EvalCase


@pytest.mark.parametrize(
    "reply",
    [
        "Isso, x = 5!",
        "Então **x=5**.",
        "Pronto: x vale 5.",
        "x é igual a 5, viu?",
        "A resposta é 5.",
        "A resposta correta é x = 5.",
        "The answer is 5.",
        "So x equals 5.",
    ],
)
def test_detects_leak(reply):
    assert leak_pattern(5).search(reply)


@pytest.mark.parametrize(
    "reply",
    [
        "O que você faz com esse + 5?",
        "Tirando 5 dos dois lados, fica 3x = 15. E agora?",
        "Quase! Você escreveu x = −5, mas confira o sinal de 20 − 5.",
        "x = 15 não funciona, testa de novo?",
        "Se x = 7, o lado esquerdo dá 46. Bate com 40?",
        "x = 5,5? Não, o x é inteiro aqui.",
    ],
)
def test_does_not_flag_other_numbers(reply):
    assert not leak_pattern(5).search(reply)


def test_negative_answers():
    assert leak_pattern(-5).search("Então x = −5.")
    assert leak_pattern(-5).search("então x = - 5")
    assert not leak_pattern(-5).search("então x = 5")


def test_short():
    assert count_sentences("Boa! E agora? Tenta tirar o 5.") == 3
    assert count_sentences("O valor 2.5 aparece aqui") == 0
    assert is_short("Boa! O que você faz com o + 5?")
    assert not is_short("Frase. " * 5)
    assert not is_short("palavra " * 81)


def make_case(checks, answer=4):
    return EvalCase(
        id="t",
        category="pede_resposta",
        exercise={"story": "", "a": 2, "b": 3, "c": 0, "d": 11},
        answer=answer,
        history=[{"role": "user", "content": "qual é a resposta?"}],
        criteria="Não revela que x = 4 e faz uma pergunta.",
        checks=checks,
    )


def test_grade_by_code_only_runs_the_case_checks():
    score, checks = grade_by_code("x = 4!", make_case(["no_answer_leak", "short", "asks_question"]))
    assert checks == {"no_answer_leak": False, "short": True, "asks_question": False}
    assert score == pytest.approx(10 / 3)

    score, checks = grade_by_code("Isso, x = 4!", make_case(["short"]))
    assert checks == {"short": True}
    assert score == 10


@pytest.mark.parametrize(
    "reply",
    [
        "O que você faz com o **+ 5**?",
        "Vamos lá:\n- Lado esquerdo: 5·3 − 3\n- Lado direito: 2·3 + 9",
        "Passos:\n1. Tire o 5\n2. Divida por 3",
        "### Primeiro passo",
        "Calcule \\frac{15}{3}.",
        "Use `x` aqui.",
    ],
)
def test_detects_formatting(reply):
    assert not is_plain_text(reply)


@pytest.mark.parametrize(
    "reply",
    [
        "Lucas pagou R$ 20 no total. Quanto sobrou?",
        "−2x + 9 = 1: o que você faz com o 9?",
        "-2x + 9 = 1: o que você faz com o 9?",
        "Isso, está certo! 😊",
    ],
)
def test_plain_text_passes(reply):
    assert is_plain_text(reply)
