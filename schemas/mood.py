# ============================================================
# schemas/mood.py — Validation des humeurs
# ============================================================

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

# On importe les codes valides définis dans le modèle
# comme ça, si on ajoute un code là-bas, ça se met à jour partout
from models.mood import MOOD_CODES


class MoodCreate(BaseModel):
    """
    Données attendues pour enregistrer une humeur (POST /api/moods).

    Exemple de payload JSON envoyé par le front :
    {
        "mood_code": "ANXIOUS",
        "free_text": "Je dors mal et je suis sous pression"
    }
    """

    # Enum implicite : on accepte seulement les codes définis dans MOOD_CODES
    mood_code: str = Field(..., description=f"Code humeur parmi : {list(MOOD_CODES.keys())}")

    # Texte libre : optionnel, limité à 1000 caractères
    free_text: Optional[str] = Field(None, max_length=1000)

    # @field_validator : une fonction qui valide un champ spécifique
    # Elle est appelée automatiquement par Pydantic à chaque validation
    @field_validator("mood_code")
    @classmethod
    def valider_mood_code(cls, valeur):
        """Vérifie que le mood_code est dans la liste des codes autorisés."""
        # On met en majuscules pour être souple (accepter "anxious" et "ANXIOUS")
        valeur = valeur.upper()
        if valeur not in MOOD_CODES:
            # Si le code est invalide, on lève une erreur avec un message clair
            raise ValueError(f"Code humeur invalide. Valeurs acceptées : {list(MOOD_CODES.keys())}")
        return valeur


class MoodOut(BaseModel):
    """Ce que l'API renvoie après avoir enregistré une humeur."""
    id:          int
    user_id:     int
    mood_code:   str
    score:       float
    free_text:   Optional[str]
    inserted_at: Optional[datetime]

    class Config:
        from_attributes = True
