# ============================================================
# routers/questionnaires.py — Routes API questionnaires
# ============================================================
# Routes gérées ici :
#   GET  /api/questionnaire/{source}          → liste des questions
#   GET  /api/questionnaire/{source}/next     → prochaine question non répondue
#   POST /api/questionnaire-answers           → enregistrer une réponse
#   GET  /api/questionnaire/progress?user_id  → avancement utilisateur

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.user import User
from models.questionnaire import QuestionnaireItem, QuestionnaireAnswer
from schemas.questionnaire import (
    QuestionnaireItemOut, QuestionnaireAnswerCreate,
    QuestionnaireAnswerOut, QuestionnaireSummary
)

router = APIRouter()

# Sources valides
SOURCES_VALIDES = ["copsoq", "whocol"]


@router.get("/questionnaire/{source}", response_model=List[QuestionnaireItemOut])
def get_questionnaire(source: str, db: Session = Depends(get_db)):
    """
    Retourne toutes les questions actives d'un questionnaire.

    - source : "copsoq" ou "whocol"

    Exemple :
      GET /api/questionnaire/copsoq → les 46 questions COPSOQ
      GET /api/questionnaire/whocol → les 22 questions WHOCOL
    """
    if source not in SOURCES_VALIDES:
        raise HTTPException(
            status_code=400,
            detail=f"Source invalide. Valeurs acceptées : {SOURCES_VALIDES}"
        )

    questions = (
        db.query(QuestionnaireItem)
        .filter(QuestionnaireItem.source == source, QuestionnaireItem.is_active == True)
        .all()
    )
    return questions


@router.get("/questionnaire/{source}/next", response_model=List[QuestionnaireItemOut])
def get_next_questionnaire_questions(
    source: str,
    user_id: int,
    batch_size: int = 5,
    db: Session = Depends(get_db)
):
    """
    Retourne le prochain lot de questions non encore répondues.

    Utile pour afficher le questionnaire par petites tranches
    plutôt que d'afficher les 46 questions d'un coup.

    - source     : "copsoq" ou "whocol"
    - batch_size : nombre de questions à retourner (défaut : 5)
    """
    if source not in SOURCES_VALIDES:
        raise HTTPException(status_code=400, detail=f"Source invalide : {source}")

    # Vérifier que l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur {user_id} introuvable")

    # Questions répondues récemment (dans les 90 derniers jours)
    # On ne re-propose pas une question déjà répondue dans cette période.
    # Après 90 jours, toutes les questions sont re-proposées pour enrichir l'historique.
    seuil = datetime.utcnow() - timedelta(days=90)

    repondues_recemment = (
        db.query(QuestionnaireAnswer.question_code)
        .filter(
            QuestionnaireAnswer.user_id    == user_id,
            QuestionnaireAnswer.source     == source,
            QuestionnaireAnswer.inserted_at >= seuil
        )
        .distinct()
        .all()
    )
    codes_repondus_recemment = {r[0] for r in repondues_recemment}

    # Récupérer les questions non répondues récemment
    questions = (
        db.query(QuestionnaireItem)
        .filter(
            QuestionnaireItem.source    == source,
            QuestionnaireItem.is_active == True,
            QuestionnaireItem.code.notin_(codes_repondus_recemment)
        )
        .limit(batch_size)
        .all()
    )

    return questions


@router.post("/questionnaire-answers", response_model=QuestionnaireAnswerOut, status_code=201)
def create_questionnaire_answer(
    user_id: int,
    payload: QuestionnaireAnswerCreate,
    db: Session = Depends(get_db)
):
    """
    Enregistre la réponse d'un utilisateur à une question COPSOQ ou WHOCOL.

    Le front envoie l'index de la réponse (0 à 4).
    Le back calcule le score correspondant depuis le catalogue.

    Exemple :
    POST /api/questionnaire-answers?user_id=42
    {
        "question_code": "copsoq7",
        "reponse_index": 2
    }
    """
    # Vérifier l'utilisateur
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur {user_id} introuvable")

    # Retrouver la question dans le catalogue
    question = db.query(QuestionnaireItem).filter(
        QuestionnaireItem.code == payload.question_code
    ).first()
    if not question:
        raise HTTPException(
            status_code=404,
            detail=f"Question '{payload.question_code}' introuvable dans le catalogue"
        )

    # Vérifier que l'index est valide pour cette question
    # (certaines questions n'ont que 4 modalités, pas 5)
    try:
        score = question.score_pour_reponse(payload.reponse_index)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Toujours créer une nouvelle réponse — on ne supprime jamais l'historique.
    # L'engine/decision.py utilise la réponse la plus récente par question
    # pour calculer le score. Les anciennes réponses restent pour l'analyse longitudinale.
    new_answer = QuestionnaireAnswer(
        user_id       = user_id,
        source        = question.source,
        question_code = payload.question_code,
        score         = score,
        reponse_index = payload.reponse_index,
        inserted_at   = datetime.utcnow(),
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer


@router.get("/questionnaire/progress", response_model=List[QuestionnaireSummary])
def get_questionnaire_progress(user_id: int, db: Session = Depends(get_db)):
    """
    Retourne l'avancement de l'utilisateur dans chaque questionnaire.

    Exemple de réponse :
    [
        {"source": "copsoq", "total": 46, "answered": 12, "completion": 26.1, "score": 67.5},
        {"source": "whocol", "total": 22, "answered": 0,  "completion": 0.0,  "score": null}
    ]
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur {user_id} introuvable")

    summaries = []
    for source in SOURCES_VALIDES:
        # Total de questions disponibles pour cette source
        total = db.query(QuestionnaireItem).filter(
            QuestionnaireItem.source    == source,
            QuestionnaireItem.is_active == True
        ).count()

        # Réponses de l'utilisateur pour cette source
        # Compter les questions distinctes répondues récemment (90j)
        seuil_prog = datetime.utcnow() - timedelta(days=90)
        reponses_recentes = (
            db.query(QuestionnaireAnswer.question_code)
            .filter(
                QuestionnaireAnswer.user_id     == user_id,
                QuestionnaireAnswer.source      == source,
                QuestionnaireAnswer.inserted_at >= seuil_prog
            )
            .distinct()
            .all()
        )
        answered = len(reponses_recentes)
        # Pour le score global, prendre la dernière réponse par question
        reponses = db.query(QuestionnaireAnswer).filter(
            QuestionnaireAnswer.user_id == user_id,
            QuestionnaireAnswer.source  == source,
            QuestionnaireAnswer.inserted_at >= seuil_prog
        ).all()
        completion = round((answered / total * 100) if total > 0 else 0.0, 1)

        # Score moyen (seulement si au moins une réponse)
        score_global = None
        if reponses:
            score_global = round(sum(r.score for r in reponses) / answered, 1)

        summaries.append(QuestionnaireSummary(
            source             = source,
            total_questions    = total,
            answered           = answered,
            completion_percent = completion,
            score_global       = score_global,
        ))

    return summaries


@router.delete("/questionnaire-answers/{source}", status_code=200)
def reset_questionnaire(source: str, user_id: int, db: Session = Depends(get_db)):
    """
    Force la réinitialisation du cycle : marque toutes les réponses comme anciennes
    en les antidatant, ce qui permet de re-proposer toutes les questions immédiatement.
    Les données historiques sont conservées.

    DELETE /api/questionnaire-answers/copsoq?user_id=42
    """
    if source not in SOURCES_VALIDES:
        raise HTTPException(status_code=400, detail=f"Source invalide. Valeurs : {SOURCES_VALIDES}")

    # Au lieu de supprimer, on antidate les réponses récentes de 91 jours
    # Elles sortent ainsi de la fenêtre des 90j → toutes les questions sont re-proposées
    # mais l'historique est conservé pour l'analyse longitudinale
    from sqlalchemy import update
    seuil_reset = datetime.utcnow() - timedelta(days=90)

    reponses_recentes = db.query(QuestionnaireAnswer).filter(
        QuestionnaireAnswer.user_id     == user_id,
        QuestionnaireAnswer.source      == source,
        QuestionnaireAnswer.inserted_at >= seuil_reset
    ).all()

    ancienne_date = datetime.utcnow() - timedelta(days=91)
    for r in reponses_recentes:
        r.inserted_at = ancienne_date

    db.commit()
    return {
        "message": f"Cycle réinitialisé pour {source} ({len(reponses_recentes)} réponses antidatées)",
        "source":  source,
        "reset":   len(reponses_recentes)
    }
