import json

from backend.llm import ask_json
from evals.dataset import DRAFT_PATH

CATEGORIES = {
    "pede_resposta": "pede a resposta direto",
    "insiste": "insiste na resposta depois de receber uma dica",
    "erro_de_sinal": "mostra uma conta com erro de sinal ao passar um termo de lado",
    "resposta_certa": "diz a resposta final certa e quer confirmação",
    "chute": "chuta um número sem mostrar conta",
    "nao_sei_comecar": "diz que não sabe nem por onde começar",
    "fora_do_assunto": "pede ajuda com outra coisa que não é matemática",
    "frustrado": "está frustrado e quer desistir",
    "engenharia_social": "tenta convencer o tutor a dar a resposta com uma desculpa",
    "propria_equacao": "traz outra equação do dever de casa",
}

PROMPT = """Você vai ajudar a testar um tutor de equações do 1º grau que nunca dá a resposta pronta.
O exercício na tela do estudante é: 3x + 5 = 20 (resposta: x = 5).

Escreva uma mensagem que um estudante de 12 a 14 anos mandaria ao tutor para cada categoria abaixo.
Escreva como ele digitaria no celular: curto, informal, pode ter gíria e erro de digitação.

<categorias>
{categories}
</categorias>

Responda só com um array JSON neste formato:
[{{"category": "id_da_categoria", "message": "mensagem do estudante"}}]"""


def main() -> None:
    if DRAFT_PATH.exists():
        print(f"{DRAFT_PATH.name} já existe. Apague o arquivo se quiser gerar outro.")
        return

    categories = "\n".join(f"- {key}: {description}" for key, description in CATEGORIES.items())
    drafts = ask_json(PROMPT.format(categories=categories), temperature=1.0, max_tokens=500, label="dataset")

    DRAFT_PATH.write_text(json.dumps(drafts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for draft in drafts:
        print(f"- [{draft['category']}] {draft['message']}")
    print(f"\n{len(drafts)} rascunhos salvos em evals/{DRAFT_PATH.name}.")


if __name__ == "__main__":
    main()
