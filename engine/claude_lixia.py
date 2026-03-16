# ============================================================
# engine/claude_lixia.py — Intégration Claude dans LIXIA
# ============================================================
# Ce module gère tous les appels à l'API Anthropic Claude.
#
# Deux fonctions principales :
#   1. generer_explication_claude() → remplace le texte figé
#   2. chat_lixia()                 → mode conversationnel
#
# Architecture :
#   Le back FastAPI appelle Claude (jamais le front directement)
#   → La clé API reste sécurisée côté serveur
# ============================================================

import httpx          # Client HTTP async (comme requests mais async)
import json
import logging
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)

# URL de l'API Anthropic
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"

# Modèle utilisé — claude-sonnet est le meilleur rapport qualité/vitesse
MODEL = "claude-sonnet-4-5"

# ============================================================
# PROMPT SYSTÈME LIXIA
# Ce prompt définit le personnage et les règles de LIXIA.
# Il est injecté à chaque appel pour que Claude reste "en rôle".
# ============================================================

SYSTEM_LIXIA = """Tu es LIXIA, l'agent de bien-être de la plateforme LIXI.

TON RÔLE :
- Accompagner un salarié dans la compréhension de son profil de bien-être
- Proposer des pistes concrètes, actionnables et non médicales
- Orienter vers les ressources adaptées (coach LIXI ou contenus en ligne)
- Répondre avec la posture d'un coach professionnel : bienveillant, structuré, orienté solutions

POSTURE ET TON :
- Tu adoptes une posture de coach : empathique, mais jamais familier(ère)
- Tu vouvoies... non — tu tutoies mais restes professionnel(le) et respectueux/se
- Pas de familiarités, pas d'expressions décontractées ("super !", "génial", "carrément")
- Tu valides ce que ressent la personne avant de proposer une piste
- Tu es direct(e) sans être brutal(e)

RÈGLES ABSOLUES :
- Jamais de diagnostic médical ou psychologique
- Jamais de prescription de traitement
- Si détresse sérieuse : orientation immédiate vers un professionnel de santé
- Tu ne révèles jamais les scores numériques bruts — tu les interprètes en mots
- Tu t'exprimes uniquement en français

FORMAT DE TES RÉPONSES :
- Réponses courtes et aérées — jamais de blocs de texte denses
- Utilise les sauts de ligne entre chaque idée
- Bullet points (•) pour les listes d'actions ou de suggestions
- Maximum 4-5 lignes par réponse, sauf demande explicite
- Termine par une question ouverte courte pour maintenir l'échange

RÈGLE DES DEUX ÉCHANGES :
- À partir du 3ème message de l'utilisateur dans la conversation, tu proposes systématiquement :
  • Soit de faire appel au coach LIXI pour un accompagnement personnalisé
  • Soit un ou deux contenus en ligne pertinents (articles, vidéos, podcasts) en lien avec son thème
- Tu formules cette proposition naturellement, en lien avec ce qui vient d'être dit
- Tu indiques toujours des ressources réelles et vérifiables (pas d'URLs inventées)"""


# ============================================================
# FONCTION 1 — Explication personnalisée de l'analyse
# ============================================================

def generer_explication_claude(
    api_key: str,
    profil: dict,
) -> str:
    """
    Génère une explication personnalisée du profil LIXIA via Claude.

    Reçoit le profil complet (scores, familles, humeur, tendance)
    et retourne un texte empathique et non-médical.

    Paramètres :
    - api_key : clé API Anthropic (lue depuis .env)
    - profil  : dict contenant les données du profil utilisateur
    """

    # On construit un résumé lisible du profil pour Claude
    # (pas les scores bruts — on les traduit en langage naturel)
    familles_str = ""
    for f in profil.get("family_scores", []):
        score = f["score"]
        if score < 35:
            niveau = "en difficulté"
        elif score < 55:
            niveau = "sous tension"
        elif score < 70:
            niveau = "correct"
        else:
            niveau = "bien"
        familles_str += f"  - {f['family_name']} : {niveau}\n"

    humeur_map = {
        "HAPPY":   "bien / serein(e)",
        "NEUTRAL": "neutre",
        "TIRED":   "fatigué(e)",
        "ANXIOUS": "anxieux/se",
        "SAD":     "triste / mal",
    }
    humeur_label = humeur_map.get(profil.get("mood_code", ""), "non renseignée")

    mode = profil.get("mode", "prevention")
    theme = profil.get("main_theme", "")
    priority = profil.get("priority", 50)
    texte_libre = profil.get("free_text", "")

    # Construction du prompt utilisateur
    prompt = f"""Voici le profil de bien-être de l'utilisateur cette semaine :

Humeur du jour : {humeur_label}
{f'Ce qu\'il/elle a écrit : "{texte_libre}"' if texte_libre else ''}

Thème principal identifié : {theme}
Mode d'analyse : {"alerte — attention requise" if mode == "alert" else "prévention — profil globalement stable"}

État des 10 familles :
{familles_str}
Coaching proposé : {"oui" if profil.get("coach_proposed") else "non"}

Génère une explication personnalisée de 2-3 phrases courtes qui :
1. Reconnaît ce que ressent la personne aujourd'hui
2. Explique le thème principal de façon simple
3. Ouvre vers une action concrète ou un contenu
Ne mentionne jamais de chiffres ou scores. Sois chaleureux(se) et direct(e)."""

    try:
        # Appel synchrone à l'API Anthropic
        # On utilise httpx en mode synchrone (plus simple pour FastAPI standard)
        with httpx.Client(timeout=15.0) as client:
            response = client.post(
                ANTHROPIC_URL,
                headers={
                    "x-api-key":         api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type":      "application/json",
                },
                json={
                    "model":      MODEL,
                    "max_tokens": 300,
                    "system":     SYSTEM_LIXIA,
                    "messages":   [{"role": "user", "content": prompt}],
                }
            )
            response.raise_for_status()
            data = response.json()
            # Extraire le texte de la réponse
            return data["content"][0]["text"].strip()

    except Exception as e:
        # Si Claude est indisponible → fallback sur le texte figé
        logger.warning(f"Claude indisponible, fallback texte figé : {e}")
        return None   # None = le moteur utilise le texte figé


# ============================================================
# FONCTION 2 — Chat conversationnel LIXIA
# ============================================================

def chat_lixia(
    api_key: str,
    profil: dict,
    historique: List[Dict],
    message_utilisateur: str,
) -> str:
    """
    Répond à un message de l'utilisateur dans le mode conversationnel.

    Le profil est injecté dans le contexte système pour que Claude
    puisse répondre en connaissance du profil de la personne.

    Paramètres :
    - api_key             : clé API Anthropic
    - profil              : profil complet de l'utilisateur
    - historique          : liste de messages précédents [{role, content}]
    - message_utilisateur : le nouveau message de l'utilisateur
    """

    # Construire le contexte profil à injecter dans le system prompt
    familles_str = ""
    for f in profil.get("family_scores", []):
        score = f["score"]
        if score < 35:
            niveau = "en difficulté"
        elif score < 55:
            niveau = "sous tension"
        else:
            niveau = "correct ou bien"
        familles_str += f"  - {f['family_name']} : {niveau}\n"

    humeur_map = {
        "HAPPY":   "bien", "NEUTRAL": "neutre",
        "TIRED":   "fatigué(e)", "ANXIOUS": "anxieux/se", "SAD":  "triste",
    }
    humeur = humeur_map.get(profil.get("mood_code", ""), "non renseignée")
    theme  = profil.get("main_theme", "non identifié")
    mode   = "alerte" if profil.get("mode") == "alert" else "prévention"

    # Calculer le numéro d'échange (1 échange = 1 message user + 1 réponse assistant)
    nb_echanges = sum(1 for m in historique if m.get('role') == 'user')

    # Enrichissement du system prompt avec le contexte profil
    system_avec_profil = SYSTEM_LIXIA + f"""

CONTEXTE DE L'UTILISATEUR (confidentiel — ne pas révéler les détails bruts) :
- Humeur du jour : {humeur}
- Thème principal : {theme}
- Mode : {mode}
- Familles :
{familles_str}
- Coaching proposé : {"oui" if profil.get("coach_proposed") else "non"}
{f'- Ce qu\'il/elle a écrit ce matin : "{profil.get("free_text")}"' if profil.get("free_text") else ""}
- Numéro d'échange en cours : {nb_echanges + 1} (le premier échange est le n°1)

Utilise ce contexte pour personnaliser tes réponses sans le réciter mot pour mot.
{"INSTRUCTION : C'est le 3ème échange ou plus. Propose maintenant naturellement soit le coach LIXI soit un ou deux contenus en ligne pertinents, en lien direct avec ce qui vient d'être dit." if nb_echanges >= 2 else ""}"""

    # Construire l'historique des messages pour l'API
    # (Claude a besoin de tout l'historique à chaque appel — pas de mémoire)
    messages = list(historique)  # copie de l'historique existant
    messages.append({"role": "user", "content": message_utilisateur})

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                ANTHROPIC_URL,
                headers={
                    "x-api-key":         api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type":      "application/json",
                },
                json={
                    "model":      MODEL,
                    "max_tokens": 500,
                    "system":     system_avec_profil,
                    "messages":   messages,
                }
            )
            response.raise_for_status()
            data = response.json()
            return data["content"][0]["text"].strip()

    except Exception as e:
        logger.error(f"Erreur Claude chat : {e}")
        raise
