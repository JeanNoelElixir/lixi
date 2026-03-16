# ============================================================
# data/seed.py — Chargement initial des données en base
# ============================================================
# Ce script remplit la base avec :
#   1. Le catalogue des questions COPSOQ et WHOCOL
#   2. Le catalogue des micro-questions (Q1 à Q20)
#
# Il est idempotent : on peut le relancer sans créer de doublons.
# "Idempotent" = même résultat qu'on le lance 1 ou 10 fois.
#
# Usage :
#   python data/seed.py
# ============================================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, engine, Base
from models.questionnaire import QuestionnaireItem
from models.micro_question import MicroQuestion
from data.catalogue_questionnaires import TOUTES_LES_QUESTIONS, NB_COPSOQ, NB_WHOCOL

# Micro-questions Q1-Q20 issues de l'onglet Questionnaires de l'Excel
MICRO_QUESTIONS_DATA = [
    {
        "code":         "Q1",
        "family_code":  "etat_emotionnel",
        "mood_trigger": "ANXIOUS,SAD,TIRED",
        "text":         "Comment te sens-tu émotionnellement aujourd’hui ?",
        "reponses":     ["Très détendu(e)", "Plutôt calme", "Un peu tendu(e)", "Très tendu(e)", "À bout / anxieux(se)"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q2",
        "family_code":  "etat_emotionnel",
        "mood_trigger": "ANXIOUS,SAD,TIRED",
        "text":         "As-tu eu du mal à déconnecter mentalement ?",
        "reponses":     ["Pas du tout", "Un peu", "Modérément", "Beaucoup", "En permanence"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q3",
        "family_code":  "fatigue_recuperation",
        "mood_trigger": "TIRED,SAD",
        "text":         "Comment évalues-tu ton niveau d’énergie aujourd’hui ?",
        "reponses":     ["Très bon", "Bon", "Moyen", "Faible", "Très faible"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q4",
        "family_code":  "fatigue_recuperation",
        "mood_trigger": "TIRED,SAD",
        "text":         "Te sens-tu reposé(e) en ce moment ?",
        "reponses":     ["Oui, tout à fait", "Plutôt oui", "Moyennement", "Plutôt non", "Non"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q5",
        "family_code":  "charge_mentale",
        "mood_trigger": "TIRED,ANXIOUS",
        "text":         "As-tu l’impression d’avoir trop de choses en tête ?",
        "reponses":     ["Pas du tout", "Un peu", "Assez souvent", "Très souvent", "En permanence"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q6",
        "family_code":  "charge_mentale",
        "mood_trigger": "TIRED,ANXIOUS",
        "text":         "Arrives-tu à te concentrer facilement ?",
        "reponses":     ["Très facilement", "Facilement", "Moyennement", "Difficilement", "Pas du tout"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q7",
        "family_code":  "exigences_pression",
        "mood_trigger": "TIRED,SAD",
        "text":         "Comment juges-tu ta charge de travail actuellement ?",
        "reponses":     ["Tout à fait gérable", "Plutôt gérable", "Juste limite", "Trop élevée", "Ingérable"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q8",
        "family_code":  "exigences_pression",
        "mood_trigger": "TIRED,SAD",
        "text":         "Te sens-tu sous pression ou dans l’urgence ?",
        "reponses":     ["Pas du tout", "Un peu", "Régulièrement", "Souvent", "En permanence"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q9",
        "family_code":  "autonomie_controle",
        "mood_trigger": "NEUTRAL,HAPPY,TIRED",
        "text":         "As-tu le sentiment de pouvoir organiser ton travail comme tu le souhaites ?",
        "reponses":     ["Tout à fait", "En grande partie", "Moyennement", "Très peu", "Pas du tout"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q10",
        "family_code":  "autonomie_controle",
        "mood_trigger": "NEUTRAL,HAPPY,TIRED",
        "text":         "As-tu des marges de manœuvre pour ajuster ta charge ou tes priorités ?",
        "reponses":     ["Oui, largement", "Oui, un peu", "Difficilement", "Très peu", "Pas du tout"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q11",
        "family_code":  "clarte_organisation",
        "mood_trigger": "NEUTRAL,HAPPY,TIRED",
        "text":         "Sais-tu clairement ce qui est attendu de toi en ce moment ?",
        "reponses":     ["Très clairement", "Plutôt clairement", "plus ou moins", "Pas très clairement", "Pas du tout"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q12",
        "family_code":  "clarte_organisation",
        "mood_trigger": "NEUTRAL,HAPPY,TIRED",
        "text":         "As-tu le sentiment que les priorités changent souvent ?",
        "reponses":     ["Rarement", "Parfois", "Régulièrement", "Souvent", "Tout le temps"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q13",
        "family_code":  "sante_sociale",
        "mood_trigger": "NEUTRAL,HAPPY,TIRED",
        "text":         "Te sens-tu soutenu(e) par ton entourage professionnel ?",
        "reponses":     ["Tout à fait", "Plutôt", "Moyennement", "Peu", "Pas du tout"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q14",
        "family_code":  "sante_sociale",
        "mood_trigger": "NEUTRAL,HAPPY,TIRED",
        "text":         "Les relations de travail te coûtent-elles de l’énergie ?",
        "reponses":     ["Pas du tout", "Un peu", "Moyennement", "Beaucoup", "Enormément"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q15",
        "family_code":  "management_reconnaissance",
        "mood_trigger": "NEUTRAL,HAPPY,TIRED",
        "text":         "Te sens-tu reconnu(e) pour ton travail ?",
        "reponses":     ["Tout à fait", "Plutôt", "Moyennement", "Peu", "Pas du tout"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q16",
        "family_code":  "management_reconnaissance",
        "mood_trigger": "NEUTRAL,HAPPY,TIRED",
        "text":         "Te sens-tu soutenu(e) par ton manager ?",
        "reponses":     ["Toujours", "Souvent", "Parfois", "Rarement", "Jamais"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q17",
        "family_code":  "sens_motivation",
        "mood_trigger": "NEUTRAL,HAPPY,TIRED",
        "text":         "Ton travail a-t-il du sens pour toi aujourd’hui ?",
        "reponses":     ["Beaucoup", "Assez", "Moyennement", "Peu", "Pas du tout"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q18",
        "family_code":  "sens_motivation",
        "mood_trigger": "NEUTRAL,HAPPY,TIRED",
        "text":         "Te sens-tu motivé(e) en ce moment ?",
        "reponses":     ["Très motivé(e)", "Plutôt motivé(e)", "Moyennement", "Peu motivé(e)", "Pas du tout"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q19",
        "family_code":  "equilibre_securite",
        "mood_trigger": "ANXIOUS,TIRED",
        "text":         "Arrives-tu à préserver un équilibre satisfaisant entre travail et vie personnelle ?",
        "reponses":     ["Tout à fait", "Plutôt", "Moyennement", "Difficilement", "Pas du tout"],
        "scores":       [100, 75, 50, 25, 0],
    },
    {
        "code":         "Q20",
        "family_code":  "equilibre_securite",
        "mood_trigger": "ANXIOUS,TIRED",
        "text":         "Te sens-tu inquiet(e) pour ton avenir professionnel ?",
        "reponses":     ["Pas du tout", "Un peu", "Modérément", "Beaucoup", "Enormément"],
        "scores":       [100, 75, 50, 25, 0],
    },
]


def seed_questionnaire_items(db):
    """
    Charge le catalogue COPSOQ et WHOCOL en base.
    Si un item existe déjà (même code), on le saute.
    """
    inseres  = 0
    ignores  = 0

    for q in TOUTES_LES_QUESTIONS:
        # Vérifier si la question existe déjà (idempotence)
        existe = db.query(QuestionnaireItem).filter(
            QuestionnaireItem.code == q["code"]
        ).first()

        if existe:
            ignores += 1
            continue

        item = QuestionnaireItem(
            source    = q["source"],
            code      = q["code"],
            domaine   = q["domaine"],
            categorie = q["categorie"],
            item      = q["item"],
            reponses  = q["reponses"],   # stocké en JSON automatiquement
            scores    = q["scores"],
        )
        db.add(item)
        inseres += 1

    db.commit()
    return inseres, ignores


def seed_micro_questions(db):
    """
    Charge les 20 micro-questions en base.
    Si une question existe déjà (même code), on la saute.
    """
    inseres = 0
    ignores = 0

    for q in MICRO_QUESTIONS_DATA:
        existe = db.query(MicroQuestion).filter(
            MicroQuestion.code == q["code"]
        ).first()

        if existe:
            ignores += 1
            continue

        import json as _json
        mq = MicroQuestion(
            code          = q["code"],
            text          = q["text"],
            family_code   = q["family_code"],
            mood_trigger  = q["mood_trigger"],
            reponses_json = _json.dumps(q.get("reponses", []), ensure_ascii=False),
            scores_json   = _json.dumps(q.get("scores",   []), ensure_ascii=False),
            is_active     = True,
        )
        db.add(mq)
        inseres += 1

    db.commit()
    return inseres, ignores


def run_seed():
    """Fonction principale : lance tous les seeders."""
    print("=== Seeder LIXIA ===")
    print()

    # Créer les tables si elles n'existent pas encore
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        print(f"1. Catalogue COPSOQ ({NB_COPSOQ} questions) + WHOCOL ({NB_WHOCOL} questions)...")
        ins, ign = seed_questionnaire_items(db)
        print(f"   ✅ {ins} insérées, {ign} déjà présentes")

        print(f"2. Micro-questions (Q1 à Q20)...")
        ins, ign = seed_micro_questions(db)
        print(f"   ✅ {ins} insérées, {ign} déjà présentes")

        print(f"3. Contenus santé (27 articles)...")
        ins, ign = seed_contenus(db)
        print(f"   ✅ {ins} insérés, {ign} déjà présents")

        # Vérification finale
        from models.content import Content
        nb_q  = db.query(QuestionnaireItem).count()
        nb_mq = db.query(MicroQuestion).count()
        nb_c  = db.query(Content).count()
        print()
        print(f"Base de données :")
        print(f"  questionnaire_items : {nb_q} questions")
        print(f"  micro_questions     : {nb_mq} questions")
        print(f"  contents            : {nb_c} articles")
        print()
        print("✅ Seed terminé !")

    finally:
        db.close()


# Permet d'exécuter directement : python data/seed.py
if __name__ == "__main__":
    run_seed()


def seed_contenus(db):
    """
    Charge les 27 contenus santé en base.
    Idempotent : on saute les contenus déjà présents (même titre + même thème).
    """
    # Import ici pour éviter les imports circulaires au démarrage
    from models.content import Content
    from data.catalogue_contenus import CONTENUS

    inseres = 0
    ignores = 0

    for c in CONTENUS:
        # Vérifier si ce contenu existe déjà
        existe = db.query(Content).filter(
            Content.theme_code == c["theme_code"],
            Content.title      == c["title"]
        ).first()

        if existe:
            ignores += 1
            continue

        contenu = Content(
            theme_code       = c["theme_code"],
            title            = c["title"],
            ultra_short_text = c["ultra_short_text"],
            short_text       = c["short_text"],
            long_text        = c["long_text"],
            display_order    = c["display_order"],
            status           = "published",   # Disponible immédiatement
        )
        db.add(contenu)
        inseres += 1

    db.commit()
    return inseres, ignores
