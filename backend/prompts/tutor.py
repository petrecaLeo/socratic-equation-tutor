from pathlib import Path

from backend.exercises.models import Exercise

LANGUAGE_NAMES = {
    "pt": "português do Brasil",
    "en": "inglês",
}

# Cada versão do prompt do tutor é um arquivo de texto: tutor_versions/v1.txt, v2.txt…
VERSIONS_DIR = Path(__file__).parent / "tutor_versions"
TUTOR_PROMPTS = {path.stem: path.read_text(encoding="utf-8").strip() for path in sorted(VERSIONS_DIR.glob("v*.txt"))}

ACTIVE_VERSION = "v4"

# A equação dos exemplos (v2 em diante). O gerador nunca sorteia ela: o tutor veria a resposta nos exemplos.
EXAMPLE_EQUATION = "5x + 4 = 39"


def describe_exercise(exercise: Exercise | None) -> str:
    if exercise is None:
        return "Nenhum. Ajude com a equação que o estudante trouxer."

    lines = [f"Problema: {exercise.story}"] if exercise.story else []
    # A resposta vai pronta, calculada por código: o tutor compara em vez de fazer a conta.
    lines += [
        f"Equação: {exercise.equation}",
        f"Resposta correta (não revele): x = {exercise.equation.solution}",
    ]
    return "\n".join(lines)


def build_tutor_system(language: str, exercise: Exercise | None = None, version: str = ACTIVE_VERSION) -> str:
    return TUTOR_PROMPTS[version].format(
        language=LANGUAGE_NAMES[language],
        exercise=describe_exercise(exercise),
    )
