# ============================================================
# engine/confidence.py — Calcul de l'indice de confiance
# ============================================================
# Formule (onglet "Règles", lignes 41-46) :
#
#   confidence = 0.35 * coverage
#              + 0.25 * recency
#              + 0.25 * volume
#              + 0.15 * consistency
#
# Plus la confiance est haute, plus l'analyse est fiable.
# ============================================================

from datetime import datetime, timedelta
from typing import Optional


def calculer_coverage(
    has_mood: bool,
    has_micro: bool,
    has_copsoq: bool,
    has_whocol: bool,
) -> float:
    """
    Coverage = combien de sources de données sont disponibles.

    Règle : 1 point par source présente, puis mis à l'échelle 0-100.
    4 sources présentes → 100, 3 → 75, 2 → 50, 1 → 25, 0 → 0.
    """
    # Compte le nombre de sources disponibles (True = 1, False = 0)
    nb_sources = sum([has_mood, has_micro, has_copsoq, has_whocol])

    # Convertit en score 0-100
    return (nb_sources / 4) * 100


def calculer_recency(
    mood_date: Optional[datetime],
    micro_date: Optional[datetime],
    copsoq_date: Optional[datetime],
    whocol_date: Optional[datetime],
) -> float:
    """
    Recency = fraîcheur des données par source.

    Règles de fraîcheur (onglet Règles, ligne 43) :
      Humeur     : OK si < 8 jours
      Micro-Q    : OK si < 14 jours
      COPSOQ     : OK si < 90 jours
      WHOCOL     : OK si < 180 jours
    Score 100 si dans l'intervalle, 0 sinon.
    Si source absente → ignorée dans la moyenne.
    """
    now = datetime.utcnow()

    # Seuils de fraîcheur en jours pour chaque source
    seuils = {
        "mood":    (mood_date,   8),
        "micro":   (micro_date, 14),
        "copsoq":  (copsoq_date, 90),
        "whocol":  (whocol_date, 180),
    }

    scores_recency = []
    for source, (date, jours_max) in seuils.items():
        if date is None:
            continue  # Source absente → on l'ignore
        age_jours = (now - date).days
        # 100 si dans le délai, 0 sinon
        scores_recency.append(100 if age_jours <= jours_max else 0)

    if not scores_recency:
        return 0.0

    return sum(scores_recency) / len(scores_recency)


def calculer_volume(nb_semaines_suivi: int) -> float:
    """
    Volume = nombre de semaines de suivi disponibles.

    Règles (onglet Règles, ligne 44) :
      1 semaine   → 20
      2 à 3 sem.  → 40
      4 à 7 sem.  → 70
      8 sem. et + → 100
    """
    if nb_semaines_suivi >= 8:
        return 100.0
    elif nb_semaines_suivi >= 4:
        return 70.0
    elif nb_semaines_suivi >= 2:
        return 40.0
    elif nb_semaines_suivi == 1:
        return 20.0
    else:
        return 0.0  # Aucun historique


def calculer_consistency(
    mood_score: Optional[float],
    copsoq_score: Optional[float],
) -> float:
    """
    Consistency = cohérence entre les sources.

    Règle (onglet Règles, ligne 45) :
      Si mood < 25 et COPSOQ > 70 → contradiction forte
      Si mood > 70 et COPSOQ < 40 → contradiction forte
      2 contradictions fortes → 40
      1 contradiction forte   → 70
      Aucune                  → 100
    """
    if mood_score is None or copsoq_score is None:
        # Pas assez de sources pour détecter une contradiction
        return 100.0

    contradictions = 0

    # Contradiction 1 : humeur très basse mais COPSOQ fort
    if mood_score < 25 and copsoq_score > 70:
        contradictions += 1

    # Contradiction 2 : humeur haute mais COPSOQ faible
    if mood_score > 70 and copsoq_score < 40:
        contradictions += 1

    # Score selon le nombre de contradictions
    if contradictions >= 2:
        return 40.0
    elif contradictions == 1:
        return 70.0
    else:
        return 100.0


def calculer_confidence(
    has_mood: bool,
    has_micro: bool,
    has_copsoq: bool,
    has_whocol: bool,
    mood_date: Optional[datetime],
    micro_date: Optional[datetime],
    copsoq_date: Optional[datetime],
    whocol_date: Optional[datetime],
    nb_semaines_suivi: int,
    mood_score: Optional[float],
    copsoq_score_global: Optional[float],
) -> dict:
    """
    Calcule l'indice de confiance global (0-100).

    Retourne un dict avec le score et le niveau ('haute', 'moyenne', 'faible').
    """

    coverage    = calculer_coverage(has_mood, has_micro, has_copsoq, has_whocol)
    recency     = calculer_recency(mood_date, micro_date, copsoq_date, whocol_date)
    volume      = calculer_volume(nb_semaines_suivi)
    consistency = calculer_consistency(mood_score, copsoq_score_global)

    # Formule pondérée de la spec
    confidence = (
        0.35 * coverage +
        0.25 * recency  +
        0.25 * volume   +
        0.15 * consistency
    )
    confidence = round(confidence, 1)

    # Niveau de confiance (onglet Règles, ligne 46)
    if confidence >= 75:
        niveau = "haute"
    elif confidence >= 50:
        niveau = "moyenne"
    else:
        niveau = "faible"

    return {
        "score":       confidence,
        "niveau":      niveau,
        # Détail des sous-scores (utile pour le débogage)
        "detail": {
            "coverage":    round(coverage, 1),
            "recency":     round(recency, 1),
            "volume":      round(volume, 1),
            "consistency": round(consistency, 1),
        }
    }
