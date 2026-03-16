# ============================================================
# engine/priority.py — Calcul de la priorité par famille
# ============================================================
# Formule (onglet "Règles", lignes 49-56) :
#
#   raw_priority = severity + trend_bonus + shock_bonus
#               + signal_bonus + recency_penalty
#   priority     = clamp(raw_priority * confidence_factor, 0, 100)
#
# La priorité exprime l'urgence de traiter une famille maintenant.
# ============================================================

from typing import Optional


def calculer_severity(score: float) -> float:
    """
    Severity = urgence de base selon le score de la famille.

    Règle (onglet Règles, ligne 50) :
      score >= 70  → 10  (tout va bien)
      score 50-69  → 40  (vigilance)
      score < 50   → 70  (critique)
      score < 35   → 85  (très critique)
      score < 20   → 95  (alarme)
    """
    if score >= 70:
        return 10.0
    elif score >= 50:
        return 40.0
    elif score >= 35:
        return 70.0
    elif score >= 20:
        return 85.0
    else:
        return 95.0


def calculer_trend_bonus(delta_4w: Optional[float]) -> float:
    """
    Trend bonus = bonus/malus selon la tendance sur 4 semaines.

    delta_4w = différence entre le score actuel et il y a 4 semaines.
    Un delta négatif = dégradation (urgent), positif = amélioration.

    Règle (onglet Règles, ligne 51) :
      delta <= -15 → +15
      delta <= -10 → +10
      delta <=  -5 → +5
      delta stable (entre -5 et +5) → 0
      delta >=  +5 → -3  (légère amélioration)
      delta >= +10 → -5  (forte amélioration)
    """
    if delta_4w is None:
        return 0.0  # Pas d'historique → pas de bonus/malus

    if delta_4w <= -15:
        return 15.0
    elif delta_4w <= -10:
        return 10.0
    elif delta_4w <= -5:
        return 5.0
    elif delta_4w < 5:
        return 0.0   # Stable
    elif delta_4w < 10:
        return -3.0  # Légère amélioration
    else:
        return -5.0  # Forte amélioration


def calculer_shock_bonus(delta_1w: Optional[float]) -> float:
    """
    Shock bonus = bonus si chute brutale en 1 semaine.

    Règle (onglet Règles, ligne 52) :
      delta 1W < -15 → +20 (choc détecté)
      sinon          → 0
    """
    if delta_1w is None:
        return 0.0
    return 20.0 if delta_1w < -15 else 0.0


def calculer_signal_bonus(
    mood_score: Optional[float],
    min_micro_score: Optional[float],
    has_strong_text_tag: bool = False,
) -> float:
    """
    Signal bonus = bonus si des signaux forts sont détectés.

    Règles (onglet Règles, ligne 53) :
      mood <= 25         → +10
      mood <= 45         → +5 (seulement si pas déjà +10)
      micro_q <= 25      → +10
      tag fort (texte)   → +10
    """
    bonus = 0.0

    # Bonus humeur basse
    if mood_score is not None:
        if mood_score <= 25:
            bonus += 10.0
        elif mood_score <= 45:
            bonus += 5.0

    # Bonus micro-question très basse (signal fort)
    if min_micro_score is not None and min_micro_score <= 25:
        bonus += 10.0

    # Bonus tag fort dans le texte libre (géré en amont)
    if has_strong_text_tag:
        bonus += 10.0

    return bonus


def calculer_recency_penalty(jours_depuis_derniere_interaction: Optional[int]) -> float:
    """
    Recency penalty = pénalité si les données sont anciennes.

    Règle (onglet Règles, ligne 55) :
      <= 7 jours  → 0   (données fraîches)
      8-14 jours  → -5
      > 14 jours  → -10
    """
    if jours_depuis_derniere_interaction is None:
        return 0.0

    if jours_depuis_derniere_interaction <= 7:
        return 0.0
    elif jours_depuis_derniere_interaction <= 14:
        return -5.0
    else:
        return -10.0


def calculer_confidence_factor(confidence_score: float) -> float:
    """
    Confidence factor = coefficient appliqué à la priorité brute.
    Une faible confiance atténue la priorité pour éviter les faux positifs.

    Règle (onglet Règles, ligne 54) :
      confidence < 50   → 0.70 (on atténue fortement)
      confidence 50-74  → 0.85 (on atténue légèrement)
      confidence >= 75  → 1.00 (on fait confiance à l'analyse)
    """
    if confidence_score >= 75:
        return 1.00
    elif confidence_score >= 50:
        return 0.85
    else:
        return 0.70


def calculer_priority(
    score_famille: float,
    confidence_score: float,
    delta_4w: Optional[float] = None,
    delta_1w: Optional[float] = None,
    mood_score: Optional[float] = None,
    min_micro_score: Optional[float] = None,
    has_strong_text_tag: bool = False,
    jours_depuis_derniere_interaction: Optional[int] = None,
) -> dict:
    """
    Calcule la priorité finale d'une famille (0-100).

    Retourne un dict avec :
      - priority    : le score final
      - raw_priority: avant application du confidence_factor
      - detail      : décomposition de chaque composant
    """

    # Calculer chaque composant
    severity         = calculer_severity(score_famille)
    trend_bonus      = calculer_trend_bonus(delta_4w)
    shock_bonus      = calculer_shock_bonus(delta_1w)
    signal_bonus     = calculer_signal_bonus(mood_score, min_micro_score, has_strong_text_tag)
    recency_penalty  = calculer_recency_penalty(jours_depuis_derniere_interaction)
    conf_factor      = calculer_confidence_factor(confidence_score)

    # Priorité brute = somme de tous les composants
    raw_priority = severity + trend_bonus + shock_bonus + signal_bonus + recency_penalty

    # Priorité finale = brute * facteur de confiance, bornée entre 0 et 100
    # max(0, min(100, x)) = clamp(x, 0, 100)
    priority = max(0.0, min(100.0, raw_priority * conf_factor))

    return {
        "priority":     round(priority, 1),
        "raw_priority": round(raw_priority, 1),
        "detail": {
            "severity":        severity,
            "trend_bonus":     trend_bonus,
            "shock_bonus":     shock_bonus,
            "signal_bonus":    signal_bonus,
            "recency_penalty": recency_penalty,
            "conf_factor":     conf_factor,
        }
    }
