from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.config import FRONTEND_DIR
from backend.errors import register_error_handlers
from backend.routes import chat, exercise, health

app = FastAPI(title="Linear Equation Tutor")
register_error_handlers(app)

app.include_router(health.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(exercise.router, prefix="/api")

# Montado por último para não engolir as rotas /api.
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
