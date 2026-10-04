import json
import os
from dataclasses import dataclass

from anthropic import Anthropic
from anthropic.types import Message

from backend.config import HELPER_MODEL, PRICES

if not os.getenv("ANTHROPIC_API_KEY"):
    raise RuntimeError("Falta a ANTHROPIC_API_KEY. Copie o .env.example para .env e coloque a sua chave.")

client = Anthropic()


@dataclass
class Spending:
    total: float = 0.0


spending = Spending()


def log_cost(label: str, model: str, message: Message) -> float:
    input_price, output_price = PRICES[model]
    usage = message.usage
    cost = (usage.input_tokens * input_price + usage.output_tokens * output_price) / 1_000_000
    print(f"[{label}] tokens: {usage.input_tokens} in / {usage.output_tokens} out | cost: ${cost:.6f}")
    spending.total += cost
    if message.stop_reason == "max_tokens":
        print(f"[{label}] aviso: resposta cortada pelo max_tokens")
    return cost


def reply_text(message: Message) -> str:
    return "".join(block.text for block in message.content if block.type == "text")


def ask_json(prompt: str, *, temperature: float, max_tokens: int, label: str):
    """Pede um JSON ao modelo ajudante. Pode levantar json.JSONDecodeError."""
    response = client.messages.create(
        model=HELPER_MODEL,
        max_tokens=max_tokens,
        messages=[
            {"role": "user", "content": prompt},
            # Prefill: a resposta já começa dentro do bloco de JSON, e o stop corta no ``` que o fecharia.
            # Os modelos 4.6 em diante recusam prefill com erro 400, por isso isto roda no Haiku 4.5.
            {"role": "assistant", "content": "```json"},
        ],
        stop_sequences=["```"],
        # O SDK 1.x tirou o temperature do create(); o extra_body manda o campo direto no JSON da request.
        extra_body={"temperature": temperature},
    )
    log_cost(label, HELPER_MODEL, response)
    return json.loads(reply_text(response))
