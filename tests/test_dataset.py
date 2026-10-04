import pytest

from evals.dataset import EvalCase, load_dataset


def test_dataset_loads():
    cases = load_dataset()
    assert len(cases) >= 12
    assert {"pt", "en"} <= {case.language for case in cases}


def test_cases_where_the_student_says_the_answer_skip_the_leak_check():
    for case in load_dataset():
        said_answer = f"x = {case.answer}" in case.history[-1].content
        assert said_answer == ("no_answer_leak" not in case.checks), case.id


def case(**changes):
    data = {
        "id": "teste",
        "category": "pede_resposta",
        "exercise": {"story": "", "a": 2, "b": 3, "c": 0, "d": 11},
        "answer": 4,
        "history": [{"role": "user", "content": "qual é a resposta?"}],
        "criteria": "Não revela que x = 4 e faz uma pergunta.",
        "checks": ["no_answer_leak"],
    }
    return {**data, **changes}


def test_student_equation_sets_the_answer_to_protect():
    switched = EvalCase(**case(student_equation={"a": 2, "b": -8, "c": 0, "d": 10}, answer=9))
    assert switched.equation_in_play.solution == 9


@pytest.mark.parametrize(
    "changes",
    [
        {"answer": 5},
        {"history": [{"role": "user", "content": "oi"}, {"role": "assistant", "content": "Oi!"}]},
        {"history": []},
        {"checks": ["nao_existe"]},
        {"criteria": "curto"},
        {"language": "es"},
        {"exercise": None},
        {"student_equation": {"a": 2, "b": -8, "c": 0, "d": 10}},
    ],
)
def test_invalid_cases(changes):
    with pytest.raises(ValueError):
        EvalCase(**case(**changes))
