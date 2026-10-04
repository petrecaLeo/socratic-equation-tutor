from typing import Annotated, Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from backend.config import MAX_MESSAGE_CHARS, MAX_REQUEST_MESSAGES
from backend.exercises.models import Equation, Exercise

Language = Literal["pt", "en"]
Difficulty = Literal["easy", "medium", "hard"]
Coefficient = Annotated[int, Field(ge=-100, le=100)]


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=MAX_MESSAGE_CHARS)


class ExerciseContext(BaseModel):
    story: str = Field(default="", max_length=600)
    a: Coefficient
    b: Coefficient
    c: Coefficient
    d: Coefficient

    @model_validator(mode="after")
    def has_integer_solution(self) -> "ExerciseContext":
        if self.to_domain().equation.solution is None:
            raise ValueError("a equação precisa ter uma solução inteira")
        return self

    def to_domain(self) -> Exercise:
        return Exercise(self.story, Equation(self.a, self.b, self.c, self.d))


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1, max_length=MAX_REQUEST_MESSAGES)
    language: Language = "pt"
    exercise: ExerciseContext | None = None

    @field_validator("messages")
    @classmethod
    def ends_with_student(cls, messages: list[ChatMessage]) -> list[ChatMessage]:
        # Terminar com o tutor seria um prefill, que o Sonnet 5.5 recusa com erro 400.
        if messages[-1].role != "user":
            raise ValueError("a última mensagem precisa ser do aluno")
        return messages


class ExerciseRequest(BaseModel):
    difficulty: Difficulty = "easy"
    language: Language = "pt"
    avoid: list[Annotated[str, Field(max_length=40)]] = Field(default_factory=list, max_length=10)


class ExerciseResponse(BaseModel):
    story: str
    equation: str
    a: int
    b: int
    c: int
    d: int

    @classmethod
    def from_domain(cls, exercise: Exercise) -> "ExerciseResponse":
        equation = exercise.equation
        return cls(story=exercise.story, equation=str(equation), a=equation.a, b=equation.b, c=equation.c, d=equation.d)
