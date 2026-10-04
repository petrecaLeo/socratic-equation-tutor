import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from backend.exercises.models import Equation
from backend.schemas import ChatMessage, ExerciseContext, Language

DATASET_PATH = Path(__file__).parent / "dataset.json"
DRAFT_PATH = Path(__file__).parent / "dataset_draft.json"

Check = Literal["no_answer_leak", "short", "asks_question", "plain_text"]


class StudentEquation(BaseModel):
    a: int
    b: int
    c: int
    d: int

    def to_domain(self) -> Equation:
        return Equation(self.a, self.b, self.c, self.d)


class EvalCase(BaseModel):
    id: str
    category: str
    language: Language = "pt"
    exercise: ExerciseContext | None
    # Quando o aluno traz outra equação, é ela que está em jogo, e não a do exercício.
    student_equation: StudentEquation | None = None
    # A resposta que o tutor não pode vazar: a da equação em jogo.
    answer: int
    history: list[ChatMessage] = Field(min_length=1)
    criteria: str = Field(min_length=20)
    checks: list[Check]

    @property
    def equation_in_play(self) -> Equation | None:
        if self.student_equation:
            return self.student_equation.to_domain()
        return self.exercise.to_domain().equation if self.exercise else None

    @model_validator(mode="after")
    def consistent(self) -> "EvalCase":
        if self.history[-1].role != "user":
            raise ValueError(f"{self.id}: o histórico precisa terminar com uma fala do aluno")
        if self.equation_in_play is None:
            raise ValueError(f"{self.id}: precisa de exercise ou student_equation")
        if self.equation_in_play.solution != self.answer:
            raise ValueError(f"{self.id}: answer não bate com a equação em jogo")
        return self


def load_dataset(path: Path = DATASET_PATH) -> list[EvalCase]:
    cases = [EvalCase(**case) for case in json.loads(path.read_text(encoding="utf-8"))]
    ids = [case.id for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("há ids repetidos no dataset")
    return cases
