import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT_DIR / "frontend"

load_dotenv(ROOT_DIR / ".env")

TUTOR_MODEL = "claude-sonnet-5-5"
HELPER_MODEL = "claude-haiku-4-5"

# US$ por milhão de tokens: (entrada, saída)
PRICES = {
    TUTOR_MODEL: (2, 10),
    HELPER_MODEL: (1, 5),
}

TUTOR_MAX_TOKENS = 400

EXERCISE_MAX_TOKENS = 200
# Temperatura alta: cada história sai com um jeito diferente de contar.
EXERCISE_TEMPERATURE = 1.0
EXERCISE_ATTEMPTS = 2

MAX_MESSAGE_CHARS = 3000
MAX_REQUEST_MESSAGES = 100
# Só as últimas mensagens vão para o modelo: os tokens de entrada crescem a cada rodada.
MAX_HISTORY_MESSAGES = 20
MAX_STUDENT_MESSAGE_CHARS = 1000

# Segurança
# Hosts aceitos no cabeçalho Host: barra DNS rebinding (um site de fora fingindo ser o localhost).
ALLOWED_HOSTS = [host.strip() for host in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if host.strip()]
MAX_BODY_BYTES = 1_048_576
# Cada request ao chat ou ao gerador vira uma chamada paga: limite por IP, por minuto.
RATE_LIMIT_PER_MINUTE = 20
# A documentação automática (/docs) fica desligada, a não ser que API_DOCS=1.
API_DOCS = os.getenv("API_DOCS") == "1"
