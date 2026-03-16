# ============================================================
# routers/analysis.py — Route d'analyse LIXIA (moteur complet)
# ============================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from engine import analyser_profil
from schemas import AnalysisOut

router = APIRouter()


@router.get("/profile-analysis", response_model=AnalysisOut)
def get_profile_analysis(user_id: int, db: Session = Depends(get_db)):
    """
    Retourne l'analyse LIXIA complète pour un utilisateur.

    Le moteur (engine/decision.py) orchestre :
      1. Récupération des données (humeur, micro-Q, questionnaires)
      2. Calcul des scores des 10 familles (engine/scoring.py)
      3. Calcul de la confiance (engine/confidence.py)
      4. Calcul de la priorité (engine/priority.py)
      5. Décision finale : thème, contenu, coaching, explication
    """

    # Vérifier que l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur {user_id} introuvable")

    try:
        # Lancer le moteur LIXIA complet
        return analyser_profil(user_id=user_id, db=db)

    except ValueError as e:
        # Erreur métier (ex: pas d'humeur enregistrée)
        raise HTTPException(status_code=422, detail=str(e))

    except Exception as e:
        # Erreur inattendue → on log et on renvoie une 500
        raise HTTPException(status_code=500, detail=f"Erreur moteur LIXIA : {str(e)}")
