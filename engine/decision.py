# ============================================================
# engine/decision.py — Orchestrateur principal de LIXIA
# ============================================================
# Ce fichier assemble tous les composants du moteur.
# C'est l'unique point d'entrée : analyser_profil(user_id, db)
# ============================================================

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from engine.scoring      import calculer_tous_les_scores
from engine.claude_lixia import generer_explication_claude
from engine.confidence import calculer_confidence
from engine.priority   import calculer_priority
from schemas.analysis  import AnalysisOut, FamilyScore

FAMILY_LABELS = {
    "etat_emotionnel":           "État émotionnel & humeur",
    "fatigue_recuperation":      "Fatigue & récupération",
    "charge_mentale":            "Charge mentale & cognition",
    "sante_sociale":             "Santé sociale & soutien",
    "exigences_pression":        "Exigences & pression au travail",
    "autonomie_controle":        "Autonomie & contrôle",
    "clarte_organisation":       "Clarté & organisation",
    "management_reconnaissance": "Management & reconnaissance",
    "sens_motivation":           "Sens, motivation & satisfaction",
    "equilibre_securite":        "Équilibre de vie & sécurité",
}

FAMILLES_CRITIQUES = {
    "etat_emotionnel", "fatigue_recuperation",
    "exigences_pression", "sens_motivation",
}


def _lire_donnees_utilisateur(user_id: int, db: Session) -> dict:
    """
    Lit toutes les données brutes de l'utilisateur en base.
    Retourne un dictionnaire structuré prêt pour les calculs.

    On sépare cette lecture du calcul pour garder chaque fonction
    focalisée sur une seule responsabilité (principe de séparation).
    """
    from models.mood import Mood
    from models.micro_question import MicroAnswer
    from models.questionnaire import QuestionnaireAnswer

    now = datetime.utcnow()

    # ── Humeur la plus récente ──
    derniere_humeur = (
        db.query(Mood)
        .filter(Mood.user_id == user_id)
        .order_by(Mood.inserted_at.desc())
        .first()
    )
    mood_score = float(derniere_humeur.score) if derniere_humeur else None
    mood_date  = derniere_humeur.inserted_at if derniere_humeur else None

    # ── Micro-réponses des 14 derniers jours ──
    seuil_micro = now - timedelta(days=14)
    micro_answers = (
        db.query(MicroAnswer)
        .filter(MicroAnswer.user_id == user_id,
                MicroAnswer.inserted_at >= seuil_micro)
        .all()
    )
    # Une réponse par code (on garde la plus récente via le premier trouvé)
    micro_scores = {}
    for a in micro_answers:
        if a.question_code not in micro_scores:
            micro_scores[a.question_code] = float(a.score)

    micro_date = (
        max((a.inserted_at for a in micro_answers), default=None)
        if micro_answers else None
    )

    # ── COPSOQ : réponses des 90 derniers jours ──
    seuil_copsoq = now - timedelta(days=90)
    # On prend toutes les réponses puis on garde la plus récente par question
    # (plusieurs réponses possibles grâce à l'historique longitudinal)
    copsoq_answers_all = (
        db.query(QuestionnaireAnswer)
        .filter(QuestionnaireAnswer.user_id == user_id,
                QuestionnaireAnswer.source  == "copsoq",
                QuestionnaireAnswer.inserted_at >= seuil_copsoq)
        .order_by(QuestionnaireAnswer.inserted_at.desc())
        .all()
    )
    # Garder la réponse la plus récente par question (le dict écrase les anciennes)
    copsoq_scores_brut = {}
    for a in reversed(copsoq_answers_all):  # du plus ancien au plus récent
        copsoq_scores_brut[a.question_code] = a
    copsoq_answers = list(copsoq_scores_brut.values())
    copsoq_scores = {a.question_code: float(a.score) for a in copsoq_answers}
    copsoq_date = (
        max((a.inserted_at for a in copsoq_answers), default=None)
        if copsoq_answers else None
    )
    # Score global COPSOQ (moyenne) pour le calcul de confiance
    copsoq_global = (
        sum(copsoq_scores.values()) / len(copsoq_scores)
        if copsoq_scores else None
    )

    # ── WHOCOL : réponses des 180 derniers jours ──
    seuil_whocol = now - timedelta(days=180)
    whocol_answers_all = (
        db.query(QuestionnaireAnswer)
        .filter(QuestionnaireAnswer.user_id == user_id,
                QuestionnaireAnswer.source  == "whocol",
                QuestionnaireAnswer.inserted_at >= seuil_whocol)
        .order_by(QuestionnaireAnswer.inserted_at.desc())
        .all()
    )
    whocol_scores_brut = {}
    for a in reversed(whocol_answers_all):
        whocol_scores_brut[a.question_code] = a
    whocol_answers = list(whocol_scores_brut.values())
    whocol_scores = {a.question_code: float(a.score) for a in whocol_answers}
    whocol_date = (
        max((a.inserted_at for a in whocol_answers), default=None)
        if whocol_answers else None
    )

    # ── Historique : nombre de semaines de suivi ──
    toutes_humeurs = db.query(Mood).filter(Mood.user_id == user_id).all()
    semaines = {h.inserted_at.isocalendar()[:2] for h in toutes_humeurs}
    nb_semaines = len(semaines)

    # ── Jours depuis la dernière interaction ──
    jours_depuis = None
    if mood_date:
        jours_depuis = (now - mood_date).days

    return {
        "mood_score":    mood_score,
        "mood_date":     mood_date,
        "micro_scores":  micro_scores,
        "micro_date":    micro_date,
        "copsoq_scores": copsoq_scores,
        "copsoq_date":   copsoq_date,
        "copsoq_global": copsoq_global,
        "whocol_scores": whocol_scores,
        "whocol_date":   whocol_date,
        "nb_semaines":   nb_semaines,
        "jours_depuis":  jours_depuis,
    }


def choisir_contenu(theme_code: str, priority: float, db: Session):
    """
    Sélectionne le contenu adapté selon le thème et le niveau de priorité.

    - priority < 40  → pas de contenu (mode prévention)
    - priority 40-59 → résumé court uniquement
    - priority ≥ 60  → article complet inclus
    """
    from models.content import Content

    if priority < 40:
        return None

    contenu = (
        db.query(Content)
        .filter(Content.theme_code == theme_code, Content.status == "published")
        .order_by(Content.display_order)
        .first()
    )
    if not contenu:
        return None

    return {
        "id":               contenu.id,
        "theme_code":       contenu.theme_code,   # Requis par le schema ContentSummary
        "title":            contenu.title,
        "ultra_short_text": contenu.ultra_short_text,
        "short_text":       contenu.short_text,
        # L'article complet n'est inclus que si la priorité est assez élevée
        "long_text":        contenu.long_text if priority >= 60 else None,
    }


def verifier_cooldown_coaching(user_id: int, db: Session) -> bool:
    """Retourne True si on peut proposer le coaching (pas de demande < 7 jours)."""
    from models.coach_request import CoachRequest
    seuil = datetime.utcnow() - timedelta(days=7)
    demande = (
        db.query(CoachRequest)
        .filter(CoachRequest.user_id == user_id,
                CoachRequest.inserted_at >= seuil)
        .first()
    )
    return demande is None


def generer_explication(main_theme: str, priority: float, mode: str) -> str:
    """Génère un message d'explication court, humain et non-médical."""
    label = FAMILY_LABELS.get(main_theme, main_theme)
    if mode == "prevention":
        return (
            f"Ton profil est globalement équilibré cette semaine. "
            f"Le thème '{label}' offre encore un peu de marge de progression. "
            f"Quelques attentions préventives font toujours la différence."
        )
    elif priority >= 75:
        return (
            f"Ton profil indique une tension notable sur '{label}'. "
            f"Ce n'est pas une fatalité — des ressources existent. "
            f"Je te propose du contenu adapté et, si tu le souhaites, un accompagnement."
        )
    else:
        return (
            f"Le thème '{label}' mérite ton attention en ce moment. "
            f"Les signaux ne sont pas alarmants, mais quelques ajustements "
            f"pourraient t'aider à retrouver un meilleur équilibre."
        )


def analyser_profil(user_id: int, db: Session) -> AnalysisOut:
    """
    Fonction principale du moteur LIXIA.
    Appelée par GET /api/profile-analysis?user_id=...

    Étapes :
      1. Lire les données brutes de l'utilisateur
      2. Calculer les scores par famille (formule pondérée)
      3. Calculer la confiance globale (4 composantes)
      4. Calculer la priorité de chaque famille
      5. Identifier le thème principal (priorité max)
      6. Choisir le contenu adapté depuis le catalogue
      7. Décider si on propose le coaching
      8. Générer l'explication textuelle
      9. Assembler et retourner l'analyse
    """

    # ── Étape 1 : Lecture des données ─────────────────────
    data = _lire_donnees_utilisateur(user_id=user_id, db=db)

    # ── Étape 2 : Scores par famille ──────────────────────
    scores_data = calculer_tous_les_scores(
        mood_score    = data["mood_score"],
        micro_scores  = data["micro_scores"],
        copsoq_scores = data["copsoq_scores"],
        whocol_scores = data["whocol_scores"],
    )
    # On extrait le score final (float) de chaque famille
    scores = {fc: v["score"] for fc, v in scores_data.items()}

    # ── Étape 3 : Confiance globale ───────────────────────
    conf_result = calculer_confidence(
        has_mood            = data["mood_score"] is not None,
        has_micro           = bool(data["micro_scores"]),
        has_copsoq          = bool(data["copsoq_scores"]),
        has_whocol          = bool(data["whocol_scores"]),
        mood_date           = data["mood_date"],
        micro_date          = data["micro_date"],
        copsoq_date         = data["copsoq_date"],
        whocol_date         = data["whocol_date"],
        nb_semaines_suivi   = data["nb_semaines"],
        mood_score          = data["mood_score"],
        copsoq_score_global = data["copsoq_global"],
    )
    # calculer_confidence retourne un dict avec "score" et les détails
    confidence = conf_result["score"] if isinstance(conf_result, dict) else float(conf_result)

    # ── Étape 4 : Priorité par famille ───────────────────
    # Score min des micro-réponses (signal d'alerte si très bas)
    min_micro = min(data["micro_scores"].values()) if data["micro_scores"] else None

    family_results = []
    for family_code, score in scores.items():
        prio_result = calculer_priority(
            score_famille    = score,
            confidence_score = confidence,
            mood_score       = data["mood_score"],
            min_micro_score  = min_micro,
            jours_depuis_derniere_interaction = data["jours_depuis"],
        )
        # calculer_priority retourne un dict avec "priority" et les détails
        priority = prio_result["priority"] if isinstance(prio_result, dict) else float(prio_result)

        family_results.append({
            "family_code": family_code,
            "family_name": FAMILY_LABELS.get(family_code, family_code),
            "score":       round(score, 1),
            "priority":    round(priority, 1),
            "confidence":  round(confidence, 1),
        })

    # Trier par priorité décroissante
    family_results.sort(key=lambda x: x["priority"], reverse=True)

    # ── Étape 5 : Thème principal ─────────────────────────
    top           = family_results[0]
    main_theme    = top["family_code"]
    main_score    = top["score"]
    main_priority = top["priority"]

    # ── Étape 6 : Mode ────────────────────────────────────
    mode = "prevention" if main_priority < 40 else "alert"

    # ── Étape 7 : Coaching ────────────────────────────────
    familles_critiques_basses = [
        f for f in family_results
        if f["family_code"] in FAMILLES_CRITIQUES and f["score"] < 40
    ]
    familles_faibles = [f for f in family_results if f["score"] < 50]

    proposer_coaching = (
        main_priority >= 75
        or len(familles_critiques_basses) >= 1
        or len(familles_faibles) >= 2
    )
    if proposer_coaching:
        proposer_coaching = verifier_cooldown_coaching(user_id=user_id, db=db)

    # ── Étape 8 : Contenu depuis le catalogue ────────────
    contenu = choisir_contenu(
        theme_code = main_theme,
        priority   = main_priority,
        db         = db,
    )

    # ── Étape 9 : Explication ─────────────────────────────
    # Tenter de générer l'explication via Claude
    # Si Claude est indisponible, on utilise le fallback figé
    explication = None
    try:
        from config import settings
        if settings.ANTHROPIC_API_KEY:
            # Construire le profil à envoyer à Claude
            profil_pour_claude = {
                "mood_code":       data.get("mood_code"),
                "free_text":       data.get("free_text"),
                "main_theme":      FAMILY_LABELS.get(main_theme, main_theme),
                "mode":            mode,
                "priority":        main_priority,
                "coach_proposed":  proposer_coaching,
                "family_scores":   [
                    {"family_name": FAMILY_LABELS.get(f["family_code"], f["family_code"]), "score": f["score"]}
                    for f in family_results
                ],
            }
            explication = generer_explication_claude(
                api_key = settings.ANTHROPIC_API_KEY,
                profil  = profil_pour_claude,
            )
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"Claude explication raté : {e}")

    # Fallback si Claude indisponible ou clé absente
    if not explication:
        explication = generer_explication(main_theme, main_priority, mode)

    # ── Assemblage ────────────────────────────────────────
    return AnalysisOut(
        main_theme     = FAMILY_LABELS.get(main_theme, main_theme),
        main_score     = round(main_score, 1),
        priority       = round(main_priority, 1),
        confidence     = round(confidence, 1),
        mode           = mode,
        content        = contenu,
        coach_proposed = proposer_coaching,
        explanation    = explication,
        family_scores  = [FamilyScore(**f) for f in family_results],
    )
