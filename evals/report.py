import json
from datetime import datetime
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "results"


def summarize(results: list[dict], cost: float) -> dict:
    n = len(results)
    leak_checked = [r for r in results if "no_answer_leak" in r["checks"]]
    return {
        "code": sum(r["code_score"] for r in results) / n,
        "judge": sum(r["judge_score"] for r in results) / n,
        "final": sum(r["score"] for r in results) / n,
        "leaks": sum(not r["checks"]["no_answer_leak"] for r in leak_checked),
        "leak_checked": len(leak_checked),
        "cost": cost,
    }


def print_case(index: int, total: int, result: dict) -> None:
    failed = [name for name, ok in result["checks"].items() if not ok]
    reply = result["reply"].strip().replace("\n", "\n         ")
    print(f"\n[{index:>2}/{total}] {result['id']} ({result['category']})")
    print(f"  tutor: {reply}")
    print(f"  código {result['code_score']:.1f}" + (f" (falhou: {', '.join(failed)})" if failed else ""))
    print(f"  juiz {result['judge_score']}: {result['judge_reasoning']}")


def save_results(version: str, results: list[dict], summary: dict) -> Path:
    RESULTS_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    path = RESULTS_DIR / f"{version}-{stamp}.json"
    data = {"version": version, "date": stamp, "summary": summary, "results": results}
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def print_report(summaries: dict[str, dict], results: dict[str, list[dict]]) -> None:
    versions = list(summaries)
    header = "| | " + " | ".join(versions) + " |\n|---|" + "---|" * len(versions)

    print("\n\n=== resultado (pronto para colar no README) ===")
    print(header)
    for label, key in [("média código", "code"), ("média juiz", "judge"), ("média final", "final")]:
        print(f"| {label} | " + " | ".join(f"{summaries[v][key]:.1f}" for v in versions) + " |")
    print("| vazamentos da resposta | " + " | ".join(f"{summaries[v]['leaks']} de {summaries[v]['leak_checked']}" for v in versions) + " |")
    print("| custo da rodada | " + " | ".join(f"${summaries[v]['cost']:.4f}" for v in versions) + " |")

    categories = sorted({r["category"] for r in results[versions[0]]})
    print("\n=== média final por categoria ===")
    print(header.replace("| |", "| categoria |", 1))
    for category in categories:
        averages = []
        for version in versions:
            scores = [r["score"] for r in results[version] if r["category"] == category]
            averages.append(f"{sum(scores) / len(scores):.1f}")
        print(f"| {category} | " + " | ".join(averages) + " |")

    print(f"\ncusto total: ${sum(s['cost'] for s in summaries.values()):.6f}")
