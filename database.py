# ============================================================
# database.py — Connexion à la base de données
# ============================================================
# Supporte SQLite (développement local) ET PostgreSQL (Render)
# La variable DATABASE_URL dans .env détermine laquelle utiliser.
#
# SQLite   : sqlite:///./lixia.db          (local)
# Postgres : postgresql://user:pass@host/db (Render)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings


# Détecter le type de base de données depuis l'URL
is_sqlite = settings.DATABASE_URL.startswith("sqlite")

# Les options de connexion diffèrent selon le moteur :
# - SQLite  : check_same_thread nécessaire (thread safety)
# - Postgres: pool_pre_ping pour détecter les connexions mortes
if is_sqlite:
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # Render utilise parfois "postgres://" (ancien format)
    # SQLAlchemy 2.x exige "postgresql://" — on corrige automatiquement
    db_url = settings.DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(
        db_url,
        pool_pre_ping=True,     # Vérifie que la connexion est active
        pool_size=5,            # 5 connexions simultanées max
        max_overflow=10,        # 10 connexions supplémentaires en cas de pic
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Générateur de session — injecté automatiquement par FastAPI
    dans chaque route via Depends(get_db).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
