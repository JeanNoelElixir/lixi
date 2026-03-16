# ============================================================
# schemas/analysis.py — Réponse de l'analyse LIXIA
# ============================================================
# Ce schema représente la réponse la plus importante de l'API :
# le résultat de l'analyse LIXIA après check-in et micro-questions.
#
# C'est ce que le front affiche dans la zone de restitution.

from pydantic import BaseModel, Field
from typing import Optional, List
from schemas.content import ContentSummary


class FamilyScore(BaseModel):
    """
    Score d'une famille fonctionnelle (ex: "Fatigue & récupération").
    L'analyse LIXIA calcule un score pour chacune des 10 familles.
    """
    family_code: str          # Ex: "fatigue_recuperation"
    family_name: str          # Ex: "Fatigue & récupération"
    score:       float        # Score 0-100 (bas = problématique)
    priority:    float        # Priorité calculée 0-100 (haut = urgent)
    confidence:  float        # Confiance dans ce score 0-100


class AnalysisOut(BaseModel):
    """
    Réponse complète de l'analyse LIXIA.
    (GET /api/profile-analysis)

    Correspond exactement au contrat d'API de la spec :
    {
        "main_theme": "Exigences & pression (surcharge)",
        "priority": 82,
        "confidence": 74,
        "content": { "id": "...", "title": "..." },
        "coach_proposed": true
    }
    """

    # Thème principal identifié par LIXIA
    # C'est la famille avec la priorité la plus élevée
    main_theme: str = Field(..., description="Famille fonctionnelle principale identifiée")

    # Score de la famille principale (0-100, bas = problématique)
    main_score: float = Field(..., ge=0, le=100)

    # Niveau de priorité calculé (0-100, haut = urgent)
    priority: float = Field(..., ge=0, le=100)

    # Niveau de confiance dans l'analyse (0-100)
    # Bas si peu de données disponibles, haut si beaucoup de signaux concordants
    confidence: float = Field(..., ge=0, le=100)

    # Mode de l'analyse : "prevention" (priorité < 40) ou "alert" (priorité >= 40)
    mode: str = Field(..., description="'prevention' ou 'alert'")

    # Contenu santé recommandé par LIXIA (résumé, pas le texte complet)
    content: Optional[ContentSummary] = None

    # True si LIXIA propose un coaching (priorité >= 75 et pas de cooldown)
    coach_proposed: bool = False

    # Détail de toutes les familles analysées (pour l'affichage du profil)
    # Le front peut afficher ces scores sous forme de graphique
    family_scores: Optional[List[FamilyScore]] = None

    # Message d'explication généré par LIXIA
    # Ex: "Votre niveau de pression semble élevé cette semaine..."
    explanation: Optional[str] = None
