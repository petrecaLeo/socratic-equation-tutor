from backend.llm import ask_json
from evals.dataset import EvalCase
from evals.judge_prompt import build_judge_prompt, parse_verdict

JUDGE_MAX_TOKENS = 300
JUDGE_ATTEMPTS = 2


def grade_by_model(case: EvalCase, reply: str) -> tuple[int, str]:
    prompt = build_judge_prompt(case, reply)

    for attempt in range(1, JUDGE_ATTEMPTS + 1):
        try:
            # Temperature 0: a mesma resposta tende a receber a mesma nota.
            data = ask_json(prompt, temperature=0.0, max_tokens=JUDGE_MAX_TOKENS, label="juiz")
            return parse_verdict(data)
        except ValueError as error:
            print(f"[juiz] tentativa {attempt} descartada: {error}")

    raise RuntimeError(f"o juiz não devolveu uma nota válida para o caso {case.id}")
