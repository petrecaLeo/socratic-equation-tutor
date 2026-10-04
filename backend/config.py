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
