from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware

from backend.config import ALLOWED_HOSTS, API_DOCS, FRONTEND_DIR
from backend.errors import register_error_handlers
from backend.routes import chat, exercise, health
from backend.security import SecurityMiddleware

docs = {} if API_DOCS else {"docs_url": None, "redoc_url": None, "openapi_url": None}
app = FastAPI(title="Linear Equation Tutor", **docs)
register_error_handlers(app)

# O último adicionado roda primeiro: o Host é conferido antes de tudo.
app.add_middleware(SecurityMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)

app.include_router(health.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(exercise.router, prefix="/api")

# Montado por último para não engolir as rotas /api.
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
