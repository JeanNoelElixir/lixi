# ============================================================
# schemas/questionnaire.py — Validation des questionnaires
# ============================================================

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class QuestionnaireItemOut(BaseModel):
    """
    Ce que l'API renvoie pour une question de questionnaire.
    Inclut les libellés des réponses pour que le front les affiche.
    """
    code:      str
    source:    str
    domaine:   Optional[str]
    categorie: Optional[str]
    item:      str              # Le texte de la question
    reponses:  List[str]        # Ex: ["Toujours", "Souvent", "Parfois"...]

    class Config:
        from_attributes = True


class QuestionnaireAnswerCreate(BaseModel):
    """
    Données pour enregistrer la réponse à une question COPSOQ ou WHOCOL.

    L'utilisateur choisit une réponse parmi les options disponibles.
    Le front envoie l'index de la réponse choisie (0 = première option).
    Le back calcule le score correspondant.

    Exemple :
    POST /api/questionnaire-answers?user_id=42
    {
        "question_code": "copsoq7",
        "reponse_index": 2
    }
    → Le back trouve scores[2] = 50 et l'enregistre
    """
    question_code:  str = Field(..., description="Code de la question (ex: copsoq7)")
    reponse_index:  int = Field(..., ge=0, le=4,
                               description="Index de la réponse choisie (0 = première option)")


class QuestionnaireAnswerOut(BaseModel):
    """Ce que l'API renvoie après avoir enregistré une réponse."""
    id:            int
    user_id:       int
    source:        str
    question_code: str
    score:         float
    reponse_index: int
    inserted_at:   Optional[datetime]

    class Config:
        from_attributes = True


class QuestionnaireSummary(BaseModel):
    """
    Résumé de progression d'un utilisateur dans un questionnaire.
    Utilisé pour afficher l'avancement (ex: "12/46 questions COPSOQ complétées").
    """
    source:             str     # "copsoq" ou "whocol"
    total_questions:    int     # Nombre total de questions
    answered:           int     # Nombre de réponses enregistrées
    completion_percent: float   # 0.0 à 100.0
    score_global:       Optional[float]  # Score moyen si au moins 1 réponse
