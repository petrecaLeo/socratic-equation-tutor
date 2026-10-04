from fastapi import APIRouter

from backend.exercises.generator import generate_exercise
from backend.exercises.signing import sign
from backend.schemas import ExerciseRequest, ExerciseResponse

router = APIRouter()


@router.post("/exercise")
def new_exercise(request: ExerciseRequest) -> ExerciseResponse:
    exercise = generate_exercise(request.difficulty, request.language, request.avoid)
    return ExerciseResponse.from_domain(exercise, sign(exercise))
