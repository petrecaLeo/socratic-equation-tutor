import pytest
from pydantic import ValidationError

from backend.schemas import ChatRequest, ExerciseRequest

USER = {"role": "user", "content": "oi"}


def test_valid_chat_request():
    request = ChatRequest(messages=[USER], exercise={"story": "", "a": 2, "b": 3, "c": 0, "d": 11, "signature": None})
    assert request.exercise.signature is None


@pytest.mark.parametrize(
    "data",
    [
        {"messages": [USER], "admin": True},
        {"messages": [{**USER, "name": "x"}]},
        {"messages": [{"role": "user", "content": "a" * 1001}]},
        {"messages": [USER], "exercise": {"a": 2, "b": 3, "c": 0, "d": 11, "signature": "f" * 65}},
    ],
)
def test_rejects_unknown_fields_and_oversized_input(data):
    with pytest.raises(ValidationError):
        ChatRequest(**data)


def test_tutor_replies_can_be_longer_than_student_messages():
    ChatRequest(messages=[USER, {"role": "assistant", "content": "a" * 2000}, USER])


def test_exercise_request_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        ExerciseRequest(difficulty="easy", extra="x")
