from backend.exercises.models import Equation
from backend.prompts.tutor import LANGUAGE_NAMES

# Variedade vem do código: com temperature 1.0 sozinha, o modelo repetia o mesmo nome e o mesmo tipo de história.
NAMES = ["Ana", "Bruno", "Carla", "Diego", "Elisa", "Felipe", "Gabi", "Heitor", "Iara", "João", "Luna", "Mateus"]
THEMES = [
    "mercado", "futebol", "videogame", "cozinha", "viagem de ônibus", "temperatura",
    "mesada", "biblioteca", "festa de aniversário", "jardim", "loja de roupas", "elevador",
]

STORY_PROMPT = """Escreva um problema curto do dia a dia, de 1 ou 2 frases, para um estudante do ensino fundamental resolver com a equação {equation}.

<detalhes>
- Personagem: {name}. Tema: {theme}.
- O valor de x é {answer}, mas a história não pode revelar isso: ela termina com a pergunta que o estudante responde resolvendo a equação.
- Os números da história precisam levar exatamente a essa equação.
- Se algum número for negativo, use um contexto em que negativo faz sentido (temperatura, saldo, andar abaixo do térreo) ou o formato "pensei num número...".
- Escreva em {language}.
</detalhes>

Responda só com um objeto JSON:
{{"story": "..."}}"""


def build_story_prompt(equation: Equation, language: str, name: str, theme: str) -> str:
    return STORY_PROMPT.format(
        equation=equation,
        answer=equation.solution,
        name=name,
        theme=theme,
        language=LANGUAGE_NAMES[language],
    )
