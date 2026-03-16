# ============================================================
# schemas/coach_request.py — Validation des demandes de coaching
# ============================================================

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

# Niveaux d'urgence valides (importés depuis le modèle)
from models.coach_request import URGENCY_LEVELS


class CoachRequestCreate(BaseModel):
    """
    Données attendues pour créer une demande de coaching.
    (POST /api/coach-requests)

    Exemple de payload :
    {
        "topic": "Surcharge / pression",
        "urgency": "high",
        "context_text": "Je suis débordé depuis 3 semaines...",
        "goal_text": "Clarifier mes priorités"
    }
    """

    topic:        str           = Field(..., min_length=2, max_length=300)
    urgency:      str           = Field("medium", description="low / medium / high")
    context_text: Optional[str] = Field(None, max_length=2000)
    goal_text:    Optional[str] = Field(None, max_length=1000)

    @field_validator("urgency")
    @classmethod
    def valider_urgency(cls, valeur):
        """Vérifie que le niveau d'urgence est valide."""
        if valeur not in URGENCY_LEVELS:
            raise ValueError(f"Urgence invalide. Valeurs acceptées : {list(URGENCY_LEVELS.keys())}")
        return valeur


class CoachRequestOut(BaseModel):
    """Ce que l'API renvoie après avoir enregistré une demande de coaching."""
    id:           int
    user_id:      int
    topic:        str
    urgency:      str
    context_text: Optional[str]
    goal_text:    Optional[str]
    status:       str
    inserted_at:  Optional[datetime]

    class Config:
        from_attributes = True
