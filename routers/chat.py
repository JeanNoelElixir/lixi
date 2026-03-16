# ============================================================
# routers/chat.py — Mode conversationnel LIXIA
# ============================================================
# Routes :
#   POST /api/chat  → envoyer un message à LIXIA
#
# Le front envoie :
#   - user_id        : l'identifiant de l'utilisateur
#   - message        : le texte saisi par l'utilisateur
#   - historique     : les messages précédents de la conversation
#
# Le back :
#   1. Charge le dernier profil de l'utilisateur
#   2. Appelle Claude avec le profil + l'historique + le message
#   3. Retourne la réponse de LIXIA

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Optional

from database import get_db
from config import settings
from models.user import User
from engine.claude_lixia import chat_lixia
from engine.decision import analyser_profil

router = APIRouter()


# ── Schéma de la requête ──────────────────────────────────
class MessageChat(BaseModel):
    """
    Un message dans l'historique de la conversation.
    role = "user" ou "assistant"
    """
    role:    str   # "user" ou "assistant"
    content: str   # Le texte du message


class ChatRequest(BaseModel):
    """
    Corps de la requête POST /api/chat

    Exemple :
    {
      "message": "Pourquoi mon score est-il bas ?",
      "historique": [
        {"role": "user",      "content": "Bonjour"},
        {"role": "assistant", "content": "Bonjour ! Comment puis-je t'aider ?"}
      ]
    }
    """
    message:    str                     # Nouveau message de l'utilisateur
    historique: List[MessageChat] = []  # Historique de la conversation (peut être vide)


class ChatResponse(BaseModel):
    """Réponse de LIXIA au message de l'utilisateur."""
    reponse:    str   # Texte généré par Claude
    role:       str = "assistant"


# ── Route principale ──────────────────────────────────────
@router.post("/chat", response_model=ChatResponse)
def envoyer_message(
    user_id: int,
    payload: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Envoie un message à LIXIA et reçoit une réponse personnalisée.

    LIXIA connaît le profil de l'utilisateur (scores, humeur, thème)
    et adapte sa réponse en conséquence.

    POST /api/chat?user_id=42
    {
      "message": "Qu'est-ce que je peux faire pour mieux gérer ma charge ?",
      "historique": [...]
    }
    """

    # Vérifier que la clé API est configurée
    if not settings.ANTHROPIC_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Le mode conversationnel n'est pas encore configuré. "
                   "Ajoute ANTHROPIC_API_KEY dans le fichier .env"
        )

    # Vérifier que l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur {user_id} introuvable")

    # Charger le profil actuel de l'utilisateur
    # (on réutilise le moteur d'analyse existant)
    try:
        analyse = analyser_profil(user_id, db)
        # Convertir l'analyse en dict pour Claude
        profil = {
            "main_theme":     analyse.main_theme,
            "mode":           analyse.mode,
            "main_score":     analyse.main_score,
            "priority":       analyse.priority,
            "coach_proposed": analyse.coach_proposed,
            "mood_code":      None,  # non exposé dans AnalysisOut pour l'instant
            "free_text":      None,
            "family_scores":  [
                {"family_name": f.family_name, "score": f.score}
                for f in (analyse.family_scores or [])
            ],
        }
    except Exception:
        # Pas encore de profil → contexte minimal
        profil = {"main_theme": None, "mode": "prevention", "family_scores": []}

    # Convertir l'historique Pydantic en liste de dicts pour l'API Claude
    historique_dicts = [
        {"role": msg.role, "content": msg.content}
        for msg in payload.historique
    ]

    # Appeler Claude
    try:
        reponse = chat_lixia(
            api_key             = settings.ANTHROPIC_API_KEY,
            profil              = profil,
            historique          = historique_dicts,
            message_utilisateur = payload.message,
        )
        return ChatResponse(reponse=reponse)

    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Erreur lors de l'appel à LIXIA : {str(e)}"
        )
