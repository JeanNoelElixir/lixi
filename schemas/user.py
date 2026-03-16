# ============================================================
# schemas/user.py — Validation des données utilisateur
# ============================================================
# Un "schema" Pydantic = un contrat de données.
# Il définit exactement ce qu'on accepte EN ENTRÉE (requête)
# et ce qu'on renvoie EN SORTIE (réponse).
#
# Règle d'or : on crée plusieurs schemas pour un même objet :
#   - UserCreate  → ce que le front envoie pour CRÉER un user
#   - UserUpdate  → ce que le front envoie pour MODIFIER un user
#   - UserOut     → ce que l'API renvoie (jamais de mot de passe !)

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """
    Données attendues pour créer un utilisateur (POST /api/user).
    Tous les champs marqués sans 'Optional' sont OBLIGATOIRES.
    """

    # Field(...) = champ obligatoire avec contraintes
    # min_length / max_length = longueur min/max acceptée
    # description = texte affiché dans la doc API automatique
    first_name: str = Field(..., min_length=1, max_length=100, description="Prénom")
    last_name:  str = Field(..., min_length=1, max_length=100, description="Nom de famille")

    # EmailStr : Pydantic vérifie automatiquement que c'est un email valide
    # Ex: "bonjour" → rejeté / "jean@lixi.fr" → accepté
    email: EmailStr = Field(..., description="Adresse email unique")

    # Optional[int] = champ optionnel de type entier (peut être absent ou None)
    age: Optional[int] = Field(None, ge=18, le=99, description="Âge (18-99 ans)")

    professional_situation: Optional[str] = Field(None, max_length=200)
    company_id: Optional[str] = Field(None, max_length=100)


class UserUpdate(BaseModel):
    """
    Données pour mettre à jour un profil (tous les champs sont optionnels).
    On ne peut modifier que ce qui est envoyé — le reste reste inchangé.
    """
    first_name:             Optional[str]   = Field(None, min_length=1, max_length=100)
    last_name:              Optional[str]   = Field(None, min_length=1, max_length=100)
    age:                    Optional[int]   = Field(None, ge=18, le=99)
    professional_situation: Optional[str]   = Field(None, max_length=200)


class UserOut(BaseModel):
    """
    Ce que l'API renvoie après avoir lu/créé un utilisateur.
    ⚠️ On n'expose jamais les données sensibles ici (mot de passe, etc.)
    """
    id:                     int
    first_name:             str
    last_name:              str
    email:                  str
    age:                    Optional[int]
    professional_situation: Optional[str]
    company_id:             Optional[str]
    created_at:             Optional[datetime]

    class Config:
        # from_attributes=True permet à Pydantic de lire
        # un objet SQLAlchemy directement (pas seulement un dict)
        from_attributes = True
