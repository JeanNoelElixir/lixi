# ============================================================
# routers/micro_questions.py — Routes API micro-questions
# ============================================================
# Routes gérées ici :
#   GET  /api/micro-questions/next  → prochaine question à poser
#   POST /api/micro-answers         → enregistrer une réponse

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.user import User
from models.mood import Mood
from models.micro_question import MicroQuestion, MicroAnswer
from schemas import MicroQuestionOut, MicroAnswerCreate, MicroAnswerOut

router = APIRouter()


@router.get("/micro-questions/next", response_model=List[MicroQuestionOut])
def get_next_questions(user_id: int, db: Session = Depends(get_db)):
    """
    Retourne les 1 à 2 prochaines micro-questions à poser.

    La sélection est basée sur :
    1. La dernière humeur enregistrée (mood_trigger)
    2. Les questions auxquelles l'utilisateur n'a pas encore répondu aujourd'hui

    Si aucune humeur n'est enregistrée → on pose des questions générales.
    """
    from datetime import date, datetime

    # Vérifier que l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur {user_id} introuvable")

    # Récupérer la dernière humeur de l'utilisateur
    last_mood = (
        db.query(Mood)
        .filter(Mood.user_id == user_id)
        .order_by(Mood.inserted_at.desc())
        .first()
    )

    # Récupérer les codes des questions déjà répondues AUJOURD'HUI
    # pour ne pas reposer deux fois la même question dans la journée
    today_start = datetime.combine(date.today(), datetime.min.time())
    already_answered = (
        db.query(MicroAnswer.question_code)
        .filter(
            MicroAnswer.user_id == user_id,
            MicroAnswer.inserted_at >= today_start
        )
        .all()
    )
    # Transformer la liste de tuples [("Q7",), ("Q3",)] en set {"Q7", "Q3"}
    answered_codes = {row[0] for row in already_answered}

    # Construire la requête de sélection des questions
    query = db.query(MicroQuestion).filter(MicroQuestion.is_active == True)

    # Si une humeur est connue, privilégier les questions liées à cette humeur
    if last_mood:
        # On cherche les questions dont le mood_trigger contient le code humeur
        # Ex: mood_trigger="TIRED,ANXIOUS" → matche si l'humeur est ANXIOUS
        query = query.filter(
            MicroQuestion.mood_trigger.contains(last_mood.mood_code)
        )

    # Exclure les questions déjà répondues aujourd'hui
    if answered_codes:
        query = query.filter(MicroQuestion.code.notin_(answered_codes))

    # Limiter à 2 questions maximum (règle de la spec)
    questions = query.limit(2).all()

    # Si aucune question spécifique à l'humeur → questions générales
    if not questions:
        questions = (
            db.query(MicroQuestion)
            .filter(
                MicroQuestion.is_active == True,
                MicroQuestion.code.notin_(answered_codes) if answered_codes else True
            )
            .limit(2)
            .all()
        )

    # Désérialiser les champs JSON et construire des dicts explicites.
    # On ne peut pas assigner dynamiquement q.reponses sur un objet SQLAlchemy
    # car Pydantic (from_attributes) lit les vrais attributs du modèle,
    # pas les attributs ajoutés à la volée. On construit donc un dict propre.
    import json
    result = []
    for q in questions:
        result.append({
            "code":        q.code,
            "text":        q.text,
            "family_code": q.family_code,
            "reponses":    json.loads(q.reponses_json) if q.reponses_json else [],
            "scores":      json.loads(q.scores_json)   if q.scores_json   else [],
        })

    return result


@router.post("/micro-answers", response_model=MicroAnswerOut, status_code=201)
def create_micro_answer(user_id: int, payload: MicroAnswerCreate, db: Session = Depends(get_db)):
    """
    Enregistre la réponse d'un utilisateur à une micro-question.

    Exemple de requête :
    POST /api/micro-answers?user_id=42
    {
        "question_code": "Q7",
        "score": 25
    }
    """

    # Vérifier que l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur {user_id} introuvable")

    # Vérifier que la question existe dans le catalogue
    question = db.query(MicroQuestion).filter(
        MicroQuestion.code == payload.question_code
    ).first()
    if not question:
        raise HTTPException(
            status_code=404,
            detail=f"Question '{payload.question_code}' introuvable dans le catalogue"
        )

    # Créer et enregistrer la réponse
    new_answer = MicroAnswer(
        user_id=user_id,
        question_code=payload.question_code,
        score=payload.score
    )

    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    return new_answer
