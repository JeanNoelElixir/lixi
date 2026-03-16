# ============================================================
# engine/scoring.py — Calcul des scores par famille
# ============================================================
# Implémente la formule de la spec (onglet "Règles") :
#
#   score_famille = 0.30 * humeur
#                + 0.25 * micro_questions
#                + 0.25 * COPSOQ_famille
#                + 0.20 * WHOCOL_famille
#
# Si une source est absente, les poids sont renormalisés.
# ============================================================

from typing import Optional


# --- Mapping Matrice LIXI (onglet "Matrice LIXI") ---
# Pour chaque famille : quelles questions COPSOQ et WHOCOL l'alimentent
# Source : colonne COPSOQ et WHOCOL de la matrice Excel

FAMILY_COPSOQ = {
    "etat_emotionnel":      ["copsoq32", "copsoq33", "copsoq35", "copsoq36", "copsoq37"],
    "fatigue_recuperation": ["copsoq31", "copsoq34", "copsoq35", "copsoq33", "copsoq38"],
    "charge_mentale":       ["copsoq5",  "copsoq6",  "copsoq7",  "copsoq8"],
    "sante_sociale":        ["copsoq23", "copsoq24", "copsoq25", "copsoq26"],
    "exigences_pression":   ["copsoq1",  "copsoq2",  "copsoq3",  "copsoq4",
                             "copsoq5",  "copsoq6",  "copsoq36", "copsoq37"],
    "autonomie_controle":   ["copsoq27", "copsoq28", "copsoq29", "copsoq30"],
    "clarte_organisation":  ["copsoq7",  "copsoq8",  "copsoq13", "copsoq14",
                             "copsoq15", "copsoq16"],
    "management_reconnaissance": ["copsoq9",  "copsoq10", "copsoq11", "copsoq12",
                                  "copsoq17", "copsoq18", "copsoq19", "copsoq20",
                                  "copsoq21", "copsoq22"],
    "sens_motivation":      ["copsoq42", "copsoq43", "copsoq44", "copsoq45", "copsoq46"],
    "equilibre_securite":   ["copsoq38", "copsoq39", "copsoq40", "copsoq41"],
}

FAMILY_WHOCOL = {
    "etat_emotionnel":      ["26 (F8.1)", "7 (5.3)", "5 (F4.1)", "19 (F6.3)"],
    "fatigue_recuperation": ["3 (F1.4)",  "10 (F2.1)", "16 (F3.3)", "2 (G4)", "1 (G1)"],
    "charge_mentale":       ["7 (5.3)",   "13 (F20.1)"],
    "sante_sociale":        ["20 (F13.3)","22 (F14.4)"],
    "exigences_pression":   ["1 (G1)",    "10 (F2.1)", "16 (F3.3)"],
    "autonomie_controle":   ["17 (F10.3)","18 (F12.4)"],
    "clarte_organisation":  ["13 (F20.1)"],
    "management_reconnaissance": ["20 (F13.3)", "22 (F14.4)"],
    "sens_motivation":      ["5 (F4.1)",  "6 (F24.2)", "19 (F6.3)", "1 (G1)"],
    "equilibre_securite":   ["8 (F16.1)", "12 (F18.1)", "9 (F22.1)", "14 (F21.1)",
                             "23 (F17.3)", "24 (F19.3)"],
}

# Mapping famille → questions micro (onglet Questionnaires)
FAMILY_MICRO_QUESTIONS = {
    "etat_emotionnel":           ["Q1", "Q2"],
    "fatigue_recuperation":      ["Q3", "Q4"],
    "charge_mentale":            ["Q5", "Q6"],
    "exigences_pression":        ["Q7", "Q8"],
    "autonomie_controle":        ["Q9", "Q10"],
    "clarte_organisation":       ["Q11", "Q12"],
    "sante_sociale":             ["Q13", "Q14"],
    "management_reconnaissance": ["Q15", "Q16"],
    "sens_motivation":           ["Q17", "Q18"],
    "equilibre_securite":        ["Q19", "Q20"],
}

# Mapping humeur → familles concernées (onglet Matrice LIXI, colonne Moods)
MOOD_TO_FAMILIES = {
    "ANXIOUS": ["etat_emotionnel", "fatigue_recuperation", "charge_mentale",
                "exigences_pression", "equilibre_securite"],
    "SAD":     ["etat_emotionnel", "sens_motivation", "sante_sociale"],
    "TIRED":   ["fatigue_recuperation", "etat_emotionnel", "exigences_pression"],
    "NEUTRAL": ["etat_emotionnel", "autonomie_controle", "clarte_organisation"],
    "HAPPY":   ["sens_motivation", "sante_sociale", "management_reconnaissance"],
}

# Noms complets des familles (pour l'affichage)
FAMILY_NAMES = {
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


def moyenne_scores(scores: list[float]) -> Optional[float]:
    """
    Calcule la moyenne d'une liste de scores.
    Retourne None si la liste est vide (source absente).

    Exemple : moyenne_scores([25, 50, 75]) → 50.0
    """
    if not scores:
        return None  # Aucune donnée disponible pour cette source
    return sum(scores) / len(scores)


def score_source_famille(family_code: str, source: str,
                         scores_dict: dict[str, float]) -> Optional[float]:
    """
    Calcule la moyenne des questions d'une source (COPSOQ ou WHOCOL)
    pour une famille donnée.

    - family_code  : ex "fatigue_recuperation"
    - source       : "copsoq" ou "whocol"
    - scores_dict  : dictionnaire {question_code: score} des réponses connues

    Retourne None si aucune question de cette famille n'a de réponse.
    """

    # Récupérer la liste des codes de questions pour cette famille/source
    if source == "copsoq":
        question_codes = FAMILY_COPSOQ.get(family_code, [])
    else:
        question_codes = FAMILY_WHOCOL.get(family_code, [])

    # Collecter les scores disponibles (on ignore les questions sans réponse)
    scores_disponibles = [
        scores_dict[code]
        for code in question_codes
        if code in scores_dict
    ]

    return moyenne_scores(scores_disponibles)


def calculer_score_famille(
    family_code: str,
    mood_score: Optional[float],          # Score de l'humeur (0-100)
    micro_scores: dict[str, float],       # {question_code: score}
    copsoq_scores: dict[str, float],      # {question_code: score}
    whocol_scores: dict[str, float],      # {question_code: score}
) -> dict:
    """
    Calcule le score composite d'une famille en combinant toutes les sources.

    Formule (spec §6.1) :
      score = 0.30*humeur + 0.25*micro + 0.25*copsoq + 0.20*whocol

    Si une source manque → on renormalise les poids des sources présentes
    pour que la somme reste égale à 1.

    Retourne un dict avec :
      - score       : le score final (0-100)
      - sources     : quelles sources ont contribué
      - poids_reels : les poids effectivement appliqués
    """

    # Poids définis dans la spec
    POIDS_DEFAUT = {
        "mood":    0.30,
        "micro":   0.25,
        "copsoq":  0.25,
        "whocol":  0.20,
    }

    # --- Calculer le score de chaque source pour cette famille ---

    # Source 1 : humeur (globale, pas spécifique à la famille)
    score_mood = mood_score

    # Source 2 : micro-questions (filtrées sur la famille)
    codes_micro = FAMILY_MICRO_QUESTIONS.get(family_code, [])
    scores_micro_famille = [micro_scores[c] for c in codes_micro if c in micro_scores]
    score_micro = moyenne_scores(scores_micro_famille)

    # Source 3 : COPSOQ (questions spécifiques à la famille)
    score_copsoq = score_source_famille(family_code, "copsoq", copsoq_scores)

    # Source 4 : WHOCOL (questions spécifiques à la famille)
    score_whocol = score_source_famille(family_code, "whocol", whocol_scores)

    # --- Construire la liste des sources présentes ---
    # On ne prend que les sources qui ont un score (pas None)
    sources_presentes = {
        "mood":   score_mood,
        "micro":  score_micro,
        "copsoq": score_copsoq,
        "whocol": score_whocol,
    }
    sources_disponibles = {k: v for k, v in sources_presentes.items() if v is not None}

    if not sources_disponibles:
        # Aucune donnée → on ne peut pas calculer
        return {
            "score": None,
            "sources": [],
            "poids_reels": {}
        }

    # --- Renormaliser les poids si des sources manquent ---
    # Ex : si COPSOQ absent, on distribue son poids (0.25)
    # proportionnellement aux 3 autres sources
    poids_disponibles = {k: POIDS_DEFAUT[k] for k in sources_disponibles}
    total_poids = sum(poids_disponibles.values())

    # Renormalisation : chaque poids divisé par le total
    # Ex : mood=0.30, micro=0.25, whocol=0.20 → total=0.75
    #      poids normalisés : mood=0.40, micro=0.33, whocol=0.27
    poids_normalises = {k: v / total_poids for k, v in poids_disponibles.items()}

    # --- Calcul du score composite ---
    score_final = sum(
        poids_normalises[source] * score
        for source, score in sources_disponibles.items()
    )

    return {
        "score":       round(score_final, 1),
        "sources":     list(sources_disponibles.keys()),
        "poids_reels": {k: round(v, 3) for k, v in poids_normalises.items()},
    }


def calculer_tous_les_scores(
    mood_score: Optional[float],
    micro_scores: dict[str, float],
    copsoq_scores: dict[str, float],
    whocol_scores: dict[str, float],
) -> dict[str, dict]:
    """
    Calcule le score de TOUTES les familles.

    Retourne un dictionnaire :
    {
      "etat_emotionnel": {"score": 35.0, "sources": [...], ...},
      "fatigue_recuperation": {...},
      ...
    }
    """
    resultats = {}
    for family_code in FAMILY_NAMES.keys():
        resultats[family_code] = calculer_score_famille(
            family_code, mood_score, micro_scores, copsoq_scores, whocol_scores
        )
        # Ajouter le nom lisible
        resultats[family_code]["family_name"] = FAMILY_NAMES[family_code]

    return resultats
