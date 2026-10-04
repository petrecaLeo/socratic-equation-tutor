"""Roda a eval do tutor. Uso: python -m evals.run_eval [versões]   ex.: python -m evals.run_eval v1 v2"""

import sys

from backend.llm import spending
from backend.prompts.tutor import ACTIVE_VERSION, TUTOR_PROMPTS
from backend.tutor import ask_tutor
from evals.checks import grade_by_code
from evals.dataset import EvalCase, load_dataset
from evals.judge import grade_by_model
from evals.report import print_case, print_report, save_results, summarize


def run_case(case: EvalCase, version: str) -> dict:
    messages = [message.model_dump() for message in case.history]
    exercise = case.exercise.to_domain() if case.exercise else None
    # O mesmo ask_tutor do app: a eval mede exatamente o que o aluno receberia.
    reply = ask_tutor(messages, case.language, exercise, version)

    code_score, checks = grade_by_code(reply, case)
    judge_score, reasoning = grade_by_model(case, reply)
    return {
        "id": case.id,
        "category": case.category,
        "reply": reply,
        "code_score": code_score,
        "checks": checks,
        "judge_score": judge_score,
        "judge_reasoning": reasoning,
        "score": (code_score + judge_score) / 2,
    }


def run_version(cases: list[EvalCase], version: str) -> tuple[list[dict], dict]:
    print(f"\n\n########## {version} ##########")
    spent_before = spending.total
    results = []
    for index, case in enumerate(cases, 1):
        result = run_case(case, version)
        print_case(index, len(cases), result)
        results.append(result)
    return results, summarize(results, cost=spending.total - spent_before)


def main(versions: list[str]) -> None:
    versions = versions or [ACTIVE_VERSION]
    unknown = [version for version in versions if version not in TUTOR_PROMPTS]
    if unknown:
        sys.exit(f"Versão desconhecida: {', '.join(unknown)}. Existem: {', '.join(TUTOR_PROMPTS)}")

    cases = load_dataset()
    summaries, results = {}, {}
    for version in versions:
        results[version], summaries[version] = run_version(cases, version)
        path = save_results(version, results[version], summaries[version])
        print(f"\nresultados salvos em evals/results/{path.name}")

    print_report(summaries, results)


if __name__ == "__main__":
    main(sys.argv[1:])
