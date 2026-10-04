import re

from backend.exercises.answer_leak import leak_pattern
from evals.dataset import EvalCase

MAX_SENTENCES = 4
MAX_WORDS = 80


def count_sentences(text: str) -> int:
    return len(re.findall(r"[.!?…]+(?=\s|$)", text.strip()))


def is_short(text: str) -> bool:
    return count_sentences(text) <= MAX_SENTENCES and len(text.split()) <= MAX_WORDS


# A tela mostra texto puro (textContent): negrito, listas e títulos aparecem como asteriscos e traços.
MARKDOWN = re.compile(r"\*\*|__|`|\\(?:frac|cdot|times|\(|\[)|^\s*(?:[-*•]|\d+\.|#+)\s", re.MULTILINE)


def is_plain_text(text: str) -> bool:
    return not MARKDOWN.search(text)


CHECKS = {
    "no_answer_leak": lambda reply, case: not leak_pattern(case.answer).search(reply),
    "short": lambda reply, case: is_short(reply),
    "asks_question": lambda reply, case: "?" in reply,
    "plain_text": lambda reply, case: is_plain_text(reply),
}


def grade_by_code(reply: str, case: EvalCase) -> tuple[float, dict[str, bool]]:
    results = {name: CHECKS[name](reply, case) for name in case.checks}
    score = 10 * sum(results.values()) / len(results) if results else 10.0
    return score, results
