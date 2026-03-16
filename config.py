# ============================================================
# config.py — Configuration centrale de l'application
# ============================================================
# Ce fichier lit les variables du .env et les rend disponibles
# partout dans le projet via l'objet "settings"

from pydantic_settings import BaseSettings  # Outil qui lit automatiquement le .env


class Settings(BaseSettings):
    """
    Classe de configuration.
    Chaque attribut correspond à une variable dans le .env.
    Si la variable n'existe pas dans .env, la valeur par défaut est utilisée.
    """

    # Nom de l'app (valeur par défaut si absent du .env)
    APP_NAME: str = "LIXIA"

    # Environnement : "development" ou "production"
    APP_ENV: str = "development"

    # URL de connexion à la base de données
    DATABASE_URL: str = "sqlite:///./lixia.db"

    # Clé secrète pour les tokens de sécurité
    SECRET_KEY: str = "default_secret_change_me"

    # Clé API Anthropic pour Claude (LIXIA conversationnelle)
    ANTHROPIC_API_KEY: str = ""

    # Version de l'API
    API_VERSION: str = "1.0.0"

    class Config:
        # Indique à pydantic où trouver le fichier de configuration
        env_file = ".env"


# On crée UNE SEULE instance de Settings, utilisée partout dans le projet
# C'est comme un "panneau de contrôle" central
settings = Settings()
