# ============================================================
# main.py — Point d'entrée de l'application LIXIA
# ============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import engine, Base

from routers import users, moods, micro_questions, contents, coaching, analysis
from routers import questionnaires
from routers import chat


# Créer les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

# Lancer le seed automatiquement au démarrage
# (idempotent : ne recrée pas ce qui existe déjà)
from data.seed import run_seed
run_seed()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.API_VERSION,
    description="Agent conversationnel de suivi santé et bien-être",
)

# En production (Render), on autorise l'URL GitHub Pages + trycloudflare
# En développement, on autorise tout
from config import settings as _settings
_allowed_origins = ["*"] if _settings.APP_ENV == "development" else [
    "https://jnguignard.github.io",   # GitHub Pages (à ajuster selon ton username)
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "null",  # Pour ouvrir index.html directement depuis le disque
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # On garde * pour simplicité du POC
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users.router,           prefix="/api", tags=["Utilisateurs"])
app.include_router(moods.router,           prefix="/api", tags=["Humeurs"])
app.include_router(micro_questions.router, prefix="/api", tags=["Micro-questions"])
app.include_router(questionnaires.router,  prefix="/api", tags=["Questionnaires COPSOQ/WHOCOL"])
app.include_router(contents.router,        prefix="/api", tags=["Contenus"])
app.include_router(coaching.router,        prefix="/api", tags=["Coaching"])
app.include_router(analysis.router,        prefix="/api", tags=["Analyse LIXIA"])
app.include_router(chat.router,             prefix="/api", tags=["Chat LIXIA"])


@app.get("/", tags=["Statut"])
def root():
    return {
        "app":     settings.APP_NAME,
        "version": settings.API_VERSION,
        "status":  "ok",
        "doc":     "/docs"
    }
