# ============================================================
# schemas/micro_question.py — Validation des micro-questions
# ============================================================

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class MicroQuestionOut(BaseModel):
    """
    Ce que l'API renvoie quand elle propose une micro-question.
    (GET /api/micro-questions/next)

    Le front affiche juste le 'text' à l'utilisateur.
    Il garde le 'code' pour l'envoyer avec la réponse.
    """
    code:        str
    text:        str
    family_code: str
    reponses:    List[str] = []   # Libellés des réponses
    scores:      List[float] = [] # Scores correspondants (0–100)

    class Config:
        from_attributes = True


class MicroAnswerCreate(BaseModel):
    """
    Données attendues pour enregistrer une réponse (POST /api/micro-answers).

    Exemple de payload :
    {
        "question_code": "Q7",
        "score": 25
    }
    """

    # Code de la question à laquelle on répond
    question_code: str = Field(..., min_length=1, max_length=20)

    # Score de 0 à 100
    # ge=0 = "greater or equal" (supérieur ou égal à 0)
    # le=100 = "lower or equal" (inférieur ou égal à 100)
    score: float = Field(..., ge=0, le=100, description="Score de 0 (très négatif) à 100 (très positif)")


class MicroAnswerOut(BaseModel):
    """Ce que l'API renvoie après avoir enregistré une réponse."""
    id:            int
    user_id:       int
    question_code: str
    score:         float
    inserted_at:   Optional[datetime]

    class Config:
        from_attributes = True
