# ============================================================
# models/user.py — Table "users" (profil utilisateur)
# ============================================================
# Un "modèle" SQLAlchemy = une classe Python qui représente
# une table dans la base de données.
# Chaque attribut de la classe = une colonne dans la table.

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func          # Pour générer automatiquement la date/heure
from database import Base               # La classe parente commune à tous les modèles


class User(Base):
    """
    Table : users
    Stocke le profil de chaque utilisateur de LIXIA.
    """

    # Nom de la table dans la base de données
    __tablename__ = "users"

    # --- Colonnes de la table ---

    # Identifiant unique, auto-incrémenté (1, 2, 3...)
    # primary_key=True : c'est la clé principale, chaque ligne a un id unique
    # index=True : accélère les recherches sur cette colonne
    id = Column(Integer, primary_key=True, index=True)

    # Prénom — obligatoire (nullable=False par défaut)
    first_name = Column(String(100), nullable=False)

    # Nom de famille — obligatoire
    last_name = Column(String(100), nullable=False)

    # Âge — optionnel (nullable=True)
    age = Column(Integer, nullable=True)

    # Email — obligatoire et unique (deux users ne peuvent pas avoir le même email)
    email = Column(String(255), nullable=False, unique=True, index=True)

    # Situation professionnelle (ex: "cadre", "employé", "manager"...)
    professional_situation = Column(String(200), nullable=True)

    # Identifiant de l'entreprise (pour regrouper les users par organisation)
    company_id = Column(String(100), nullable=True)

    # Date/heure de création du compte
    # server_default=func.now() : la base remplit automatiquement avec l'heure actuelle
    created_at = Column(DateTime, server_default=func.now())

    # Date/heure de la dernière modification
    # onupdate=func.now() : mis à jour automatiquement à chaque modification
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        """Affichage lisible dans la console Python (utile pour déboguer)."""
        return f"<User id={self.id} email={self.email}>"
