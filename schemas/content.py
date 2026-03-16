# ============================================================
# schemas/content.py — Validation des contenus santé
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ContentOut(BaseModel):
    """
    Ce que l'API renvoie pour un contenu santé.
    (GET /api/contents ou GET /api/contents/:id)

    Le front peut choisir d'afficher :
    - ultra_short_text dans la carte de recommandation
    - short_text dans la zone de restitution
    - long_text quand l'utilisateur clique "Lire plus"
    """
    id:               int
    theme_code:       str
    title:            str
    ultra_short_text: Optional[str]   # Accroche courte (quelques mots)
    short_text:       Optional[str]   # Résumé (2-3 phrases)
    long_text:        Optional[str]   # Article complet
    display_order:    int

    class Config:
        from_attributes = True


class ContentSummary(BaseModel):
    """
    Contenu tel qu'il est inclus dans une réponse d'analyse.

    Le moteur décide quels champs peupler selon la priorité :
      - priorité < 60  → short_text uniquement
      - priorité ≥ 60  → short_text + long_text (article complet)

    Le front peut ainsi tout afficher sans second appel API.
    """
    id:               int
    theme_code:       str
    title:            str
    ultra_short_text: Optional[str] = None
    short_text:       Optional[str] = None   # Résumé 2-3 phrases
    long_text:        Optional[str] = None   # Article complet (si priorité ≥ 60)

    class Config:
        from_attributes = True
