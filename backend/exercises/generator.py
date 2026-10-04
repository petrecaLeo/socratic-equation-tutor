import random

from backend.config import EXERCISE_ATTEMPTS, EXERCISE_MAX_TOKENS, EXERCISE_TEMPERATURE
from backend.exercises.models import Exercise
from backend.exercises.random_equation import random_equation
from backend.exercises.validation import parse_story
from backend.llm import ask_json
from backend.prompts.exercise import NAMES, THEMES, build_story_prompt
from backend.prompts.tutor import EXAMPLE_EQUATION


class ExerciseGenerationFailed(Exception):
    pass


def generate_exercise(difficulty: str, language: str, avoid: list[str]) -> Exercise:
    # O código sorteia a equação (conta certa por construção); o modelo só escreve a história.
    equation = random_equation(difficulty, {*avoid, EXAMPLE_EQUATION})
    prompt = build_story_prompt(equation, language, random.choice(NAMES), random.choice(THEMES))

    for attempt in range(1, EXERCISE_ATTEMPTS + 1):
        try:
            data = ask_json(prompt, temperature=EXERCISE_TEMPERATURE, max_tokens=EXERCISE_MAX_TOKENS, label="exercício")
            return Exercise(parse_story(data, equation), equation)
        except ValueError as error:
            print(f"[exercício] tentativa {attempt} descartada: {error}")

    raise ExerciseGenerationFailed()
