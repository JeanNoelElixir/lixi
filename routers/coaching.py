# ============================================================
# routers/coaching.py — Routes API pour le coaching
# ============================================================
# Routes gérées ici :
#   POST /api/coach-requests → envoyer une demande de coaching

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database import get_db
from models.user import User
from models.coach_request import CoachRequest
from schemas import CoachRequestCreate, CoachRequestOut

router = APIRouter()

# Délai minimum entre deux demandes de coaching (règle "cooldown" de la spec)
# Un utilisateur ne peut pas en envoyer une nouvelle avant ce délai
COOLDOWN_DAYS = 7


@router.post("/coach-requests", response_model=CoachRequestOut, status_code=201)
def create_coach_request(user_id: int, payload: CoachRequestCreate, db: Session = Depends(get_db)):
    """
    Crée une demande de coaching pour un utilisateur.

    Règles métier :
    - L'utilisateur doit exister
    - L'utilisateur ne peut pas envoyer deux demandes en moins de 7 jours (cooldown)

    Exemple de requête :
    POST /api/coach-requests?user_id=42
    {
        "topic": "Surcharge / pression",
        "urgency": "high",
        "context_text": "Je suis débordé depuis 3 semaines",
        "goal_text": "Clarifier mes priorités"
    }
    """

    # Vérifier que l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur {user_id} introuvable")

    # Vérifier le cooldown : y a-t-il une demande récente ?
    cooldown_limit = datetime.utcnow() - timedelta(days=COOLDOWN_DAYS)
    recent_request = (
        db.query(CoachRequest)
        .filter(
            CoachRequest.user_id == user_id,
            CoachRequest.inserted_at >= cooldown_limit  # Dans les 7 derniers jours
        )
        .first()
    )

    if recent_request:
        # 429 Too Many Requests : l'utilisateur doit attendre
        jours_restants = COOLDOWN_DAYS - (datetime.utcnow() - recent_request.inserted_at).days
        raise HTTPException(
            status_code=429,
            detail=f"Une demande a déjà été envoyée. Merci de patienter encore {jours_restants} jour(s)."
        )

    # Créer la demande
    new_request = CoachRequest(
        user_id=user_id,
        topic=payload.topic,
        urgency=payload.urgency,
        context_text=payload.context_text,
        goal_text=payload.goal_text
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request
