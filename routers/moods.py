# ============================================================
# routers/moods.py — Routes API pour les humeurs
# ============================================================
# Routes gérées ici :
#   POST /api/moods              → enregistrer une humeur
#   GET  /api/moods?user_id=...  → historique des humeurs

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.user import User
from models.mood import Mood
from schemas import MoodCreate, MoodOut

router = APIRouter()


# Table de conversion : code humeur → score numérique (0-100)
# Plus le score est bas, plus l'humeur est négative
# C'est le back qui décide du score, jamais le front
MOOD_SCORES = {
    "HAPPY":   85,   # Bien / Positif
    "NEUTRAL": 55,   # Neutre
    "TIRED":   35,   # Fatigué(e)
    "ANXIOUS": 20,   # Anxieux/se
    "SAD":     15,   # Triste / Bas(se)
}


@router.post("/moods", response_model=MoodOut, status_code=201)
def create_mood(user_id: int, payload: MoodCreate, db: Session = Depends(get_db)):
    """
    Enregistre une humeur pour un utilisateur.

    - user_id : passé en paramètre d'URL → POST /api/moods?user_id=42
    - payload : le corps JSON avec mood_code et free_text optionnel

    Exemple de requête :
    POST /api/moods?user_id=42
    {
        "mood_code": "ANXIOUS",
        "free_text": "Je dors mal depuis une semaine"
    }
    """

    # Vérifier que l'utilisateur existe avant d'enregistrer son humeur
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur {user_id} introuvable")

    # Convertir le code humeur en score numérique
    # .get() renvoie None si le code n'existe pas (mais Pydantic l'a déjà validé)
    score = MOOD_SCORES.get(payload.mood_code, 50)

    # Créer l'objet Mood avec toutes ses données
    new_mood = Mood(
        user_id=user_id,
        mood_code=payload.mood_code,
        score=score,
        free_text=payload.free_text
    )

    db.add(new_mood)
    db.commit()
    db.refresh(new_mood)

    return new_mood


@router.get("/moods", response_model=List[MoodOut])
def get_moods(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retourne l'historique des humeurs d'un utilisateur.

    - limit : nombre maximum de résultats (défaut = 10, pour ne pas tout charger)

    Les humeurs sont triées de la plus récente à la plus ancienne.
    """

    # Vérifier que l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur {user_id} introuvable")

    # Récupérer les humeurs, triées par date décroissante
    # .order_by(Mood.inserted_at.desc()) = du plus récent au plus ancien
    # .limit(limit) = on ne prend que les N premiers résultats
    # .all() = exécute la requête et retourne une liste
    moods = (
        db.query(Mood)
        .filter(Mood.user_id == user_id)
        .order_by(Mood.inserted_at.desc())
        .limit(limit)
        .all()
    )

    return moods
