"""Lista todas as rodadas salvas em evals/results/. Uso: python -m evals.history"""

import json

from evals.report import RESULTS_DIR


def main() -> None:
    runs = [json.loads(path.read_text(encoding="utf-8")) for path in RESULTS_DIR.glob("*.json")]
    runs.sort(key=lambda run: (run["date"], run["version"]))

    print("| data | versão | código | juiz | final | vazamentos | custo |")
    print("|---|---|---|---|---|---|---|")
    for run in runs:
        s = run["summary"]
        date = f"{run['date'][:4]}-{run['date'][4:6]}-{run['date'][6:8]} {run['date'][9:11]}:{run['date'][11:]}"
        print(
            f"| {date} | {run['version']} | {s['code']:.1f} | {s['judge']:.1f} | {s['final']:.1f} "
            f"| {s['leaks']} de {s['leak_checked']} | ${s['cost']:.4f} |"
        )


if __name__ == "__main__":
    main()
