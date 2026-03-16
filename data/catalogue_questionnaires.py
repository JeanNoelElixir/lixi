# ============================================================
# data/catalogue_questionnaires.py — Données de référence
# ============================================================
# Ce fichier contient TOUTES les questions COPSOQ et WHOCOL
# issues de l'Excel (onglet "Questionnaires").
#
# Structure de chaque question :
#   {
#     "source":    "copsoq" ou "whocol",
#     "code":      identifiant unique,
#     "domaine":   domaine thématique,
#     "categorie": sous-catégorie,
#     "item":      texte de la question,
#     "reponses":  liste des libellés de réponse,
#     "scores":    liste des scores correspondants (0-100),
#   }
#
# Les scores sont ceux de l'Excel, colonne Q1 à Q5.
# Un score élevé = positif pour le bien-être.
# ============================================================

QUESTIONS_COPSOQ = [
    # ---- Domaine : Contraintes quantitatives ----
    {
        "source": "copsoq", "code": "copsoq1",
        "domaine": "Contraintes quantitatives", "categorie": "Charge de travail",
        "item": "Prenez-vous du retard dans votre travail ?",
        "reponses": ["Toujours", "Souvent", "Parfois", "Rarement", "Presque jamais/Jamais"],
        "scores": [0, 25, 50, 75, 100],  # Inversé : prendre du retard = mauvais
    },
    {
        "source": "copsoq", "code": "copsoq2",
        "domaine": "Contraintes quantitatives", "categorie": "Charge de travail",
        "item": "Disposez-vous d'un temps suffisant pour accomplir vos tâches professionnelles ?",
        "reponses": ["Toujours", "Souvent", "Parfois", "Rarement", "Presque jamais/Jamais"],
        "scores": [100, 75, 50, 25, 0],  # Direct : avoir du temps = bon
    },
    {
        "source": "copsoq", "code": "copsoq3",
        "domaine": "Contraintes quantitatives", "categorie": "Rythme de travail",
        "item": "Travaillez-vous à une cadence élevée tout au long de la journée ?",
        "reponses": ["Toujours", "Souvent", "Parfois", "Rarement", "Presque jamais/Jamais"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "copsoq", "code": "copsoq4",
        "domaine": "Contraintes quantitatives", "categorie": "Rythme de travail",
        "item": "Est-il nécessaire de maintenir un rythme soutenu au travail ?",
        "reponses": ["Toujours", "Souvent", "Parfois", "Rarement", "Presque jamais/Jamais"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "copsoq", "code": "copsoq5",
        "domaine": "Contraintes quantitatives", "categorie": "Exigences cognitives",
        "item": "Durant votre travail, devez-vous avoir l'œil sur beaucoup de choses ?",
        "reponses": ["Toujours", "Souvent", "Parfois", "Rarement", "Presque jamais/Jamais"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "copsoq", "code": "copsoq6",
        "domaine": "Contraintes quantitatives", "categorie": "Exigences cognitives",
        "item": "Votre travail exige-t-il que vous vous souveniez de beaucoup de choses ?",
        "reponses": ["Toujours", "Souvent", "Parfois", "Rarement", "Presque jamais/Jamais"],
        "scores": [0, 25, 50, 75, 100],
    },
    # ---- Domaine : Organisations et leadership ----
    {
        "source": "copsoq", "code": "copsoq7",
        "domaine": "Organisations et leadership", "categorie": "Prévisibilité",
        "item": "Au travail, êtes-vous informé(e) suffisamment à l'avance au sujet par exemple de décisions importantes, de changements ou de projets futurs ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq8",
        "domaine": "Organisations et leadership", "categorie": "Prévisibilité",
        "item": "Recevez-vous toutes les informations dont vous avez besoin pour bien faire votre travail ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq9",
        "domaine": "Organisations et leadership", "categorie": "Reconnaissance",
        "item": "Votre travail est-il reconnu et apprécié par le management ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq10",
        "domaine": "Organisations et leadership", "categorie": "Reconnaissance",
        "item": "Êtes-vous traité(e) équitablement au travail ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq11",
        "domaine": "Organisations et leadership", "categorie": "Équité",
        "item": "Les conflits sont-ils résolus de manière équitable ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq12",
        "domaine": "Organisations et leadership", "categorie": "Équité",
        "item": "Le travail est-il réparti équitablement ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq13",
        "domaine": "Organisations et leadership", "categorie": "Clarté des rôles",
        "item": "Votre travail a-t-il des objectifs clairs ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq14",
        "domaine": "Organisations et leadership", "categorie": "Clarté des rôles",
        "item": "Savez-vous exactement ce que l'on attend de vous au travail ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq15",
        "domaine": "Organisations et leadership", "categorie": "Conflit de rôles",
        "item": "Au travail, êtes-vous soumis(e) à des demandes contradictoires ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [0, 25, 50, 75, 100],  # Inversé : demandes contradictoires = mauvais
    },
    {
        "source": "copsoq", "code": "copsoq16",
        "domaine": "Organisations et leadership", "categorie": "Conflit de rôles",
        "item": "Devez-vous parfois faire des choses qui auraient dû être faites autrement ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "copsoq", "code": "copsoq17",
        "domaine": "Organisations et leadership", "categorie": "Qualité de leadership",
        "item": "Dans quelle mesure diriez-vous que votre supérieur(e) hiérarchique accorde une grande priorité à la satisfaction au travail ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq18",
        "domaine": "Organisations et leadership", "categorie": "Qualité de leadership",
        "item": "Dans quelle mesure diriez-vous que votre supérieur(e) hiérarchique est compétent(e) dans la planification du travail ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq19",
        "domaine": "Organisations et leadership", "categorie": "Soutien hiérarchique",
        "item": "À quelle fréquence votre supérieur(e) hiérarchique est-il(elle) disposé(e) à vous écouter au sujet de vos problèmes au travail ?",
        "reponses": ["Toujours", "Souvent", "Parfois", "Rarement", "Presque jamais/Jamais"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq20",
        "domaine": "Organisations et leadership", "categorie": "Soutien hiérarchique",
        "item": "À quelle fréquence recevez-vous de l'aide et du soutien de votre supérieur(e) hiérarchique ?",
        "reponses": ["Toujours", "Souvent", "Parfois", "Rarement", "Presque jamais/Jamais"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq21",
        "domaine": "Organisations et leadership", "categorie": "Confiance management",
        "item": "Le management fait-il confiance aux salariés quant à leur capacité à bien faire leur travail ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq22",
        "domaine": "Organisations et leadership", "categorie": "Confiance management",
        "item": "Pouvez-vous faire confiance aux informations venant du management ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    # ---- Domaine : Relations horizontales ----
    {
        "source": "copsoq", "code": "copsoq23",
        "domaine": "Relations horizontales", "categorie": "Confiance collègues",
        "item": "Y a-t-il une bonne coopération entre les collègues au travail ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq24",
        "domaine": "Relations horizontales", "categorie": "Confiance collègues",
        "item": "Dans l'ensemble, les salariés se font-ils confiance entre eux ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq25",
        "domaine": "Relations horizontales", "categorie": "Soutien collègues",
        "item": "À quelle fréquence recevez-vous de l'aide et du soutien de vos collègues ?",
        "reponses": ["Toujours", "Souvent", "Parfois", "Rarement", "Presque jamais/Jamais"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq26",
        "domaine": "Relations horizontales", "categorie": "Soutien collègues",
        "item": "À quelle fréquence vos collègues se montrent-ils à l'écoute de vos problèmes au travail ?",
        "reponses": ["Toujours", "Souvent", "Parfois", "Rarement", "Presque jamais/Jamais"],
        "scores": [100, 75, 50, 25, 0],
    },
    # ---- Domaine : Autonomie ----
    {
        "source": "copsoq", "code": "copsoq27",
        "domaine": "Autonomie", "categorie": "Marge de manœuvre",
        "item": "Avez-vous une grande marge de manœuvre dans votre travail ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq28",
        "domaine": "Autonomie", "categorie": "Marge de manœuvre",
        "item": "Pouvez-vous intervenir sur la quantité de travail qui vous est attribuée ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq29",
        "domaine": "Autonomie", "categorie": "Épanouissement",
        "item": "Votre travail nécessite-t-il que vous preniez des initiatives ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq30",
        "domaine": "Autonomie", "categorie": "Épanouissement",
        "item": "Votre travail vous donne-il la possibilité d'apprendre des choses nouvelles ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    # ---- Domaine : Santé et bien-être ----
    {
        "source": "copsoq", "code": "copsoq31",
        "domaine": "Santé et bien-être", "categorie": "Santé auto-évaluée",
        "item": "En général, diriez-vous que votre santé est :",
        "reponses": ["Excellente/Très bonne", "Bonne", "Assez bonne", "Plutôt mauvaise", "Mauvaise"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq32",
        "domaine": "Santé et bien-être", "categorie": "Stress",
        "item": "À quelle fréquence avez-vous été irritable ?",
        "reponses": ["Toujours", "Souvent", "Parfois", "Rarement", "Presque jamais/Jamais"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "copsoq", "code": "copsoq33",
        "domaine": "Santé et bien-être", "categorie": "Stress",
        "item": "À quelle fréquence avez-vous été stressé(e) ?",
        "reponses": ["Toujours", "Souvent", "Parfois", "Rarement", "Presque jamais/Jamais"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "copsoq", "code": "copsoq34",
        "domaine": "Santé et bien-être", "categorie": "Épuisement",
        "item": "À quelle fréquence vous êtes-vous senti(e) à bout de force ?",
        "reponses": ["Toujours", "Souvent", "Parfois", "Rarement", "Presque jamais/Jamais"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "copsoq", "code": "copsoq35",
        "domaine": "Santé et bien-être", "categorie": "Épuisement",
        "item": "À quelle fréquence avez-vous été émotionnellement épuisé(e) ?",
        "reponses": ["Toujours", "Souvent", "Parfois", "Rarement", "Presque jamais/Jamais"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "copsoq", "code": "copsoq36",
        "domaine": "Santé et bien-être", "categorie": "Exigences émotionnelles",
        "item": "Votre travail vous place-t-il dans des situations déstabilisantes sur le plan émotionnel ?",
        "reponses": ["Toujours", "Souvent", "Parfois", "Rarement", "Presque jamais/Jamais"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "copsoq", "code": "copsoq37",
        "domaine": "Santé et bien-être", "categorie": "Exigences émotionnelles",
        "item": "Votre travail est-il éprouvant sur le plan émotionnel ?",
        "reponses": ["Toujours", "Souvent", "Parfois", "Rarement", "Presque jamais/Jamais"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "copsoq", "code": "copsoq38",
        "domaine": "Santé et bien-être", "categorie": "Conflit famille/travail",
        "item": "Sentez-vous que votre travail vous prend tellement d'énergie que cela a un impact négatif sur votre vie privée ?",
        "reponses": ["Oui, certainement", "Oui, jusqu'à un certain point", "Oui, mais juste un peu", "Non, pas du tout"],
        "scores": [0, 33, 66, 100],  # 4 modalités uniquement
    },
    {
        "source": "copsoq", "code": "copsoq39",
        "domaine": "Santé et bien-être", "categorie": "Conflit famille/travail",
        "item": "Sentez-vous que votre travail vous prend tellement de temps que cela a un impact négatif sur votre vie privée ?",
        "reponses": ["Oui, certainement", "Oui, jusqu'à un certain point", "Oui, mais juste un peu", "Non, pas du tout"],
        "scores": [0, 33, 66, 100],
    },
    {
        "source": "copsoq", "code": "copsoq40",
        "domaine": "Santé et bien-être", "categorie": "Insécurité professionnelle",
        "item": "Êtes-vous inquiet(ète) à l'idée de perdre votre emploi ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "copsoq", "code": "copsoq41",
        "domaine": "Santé et bien-être", "categorie": "Insécurité professionnelle",
        "item": "Craignez-vous d'être muté(e) à un autre poste de travail contre votre volonté ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [0, 25, 50, 75, 100],
    },
    # ---- Domaine : Vécu professionnel ----
    {
        "source": "copsoq", "code": "copsoq42",
        "domaine": "Vécu professionnel", "categorie": "Sens du travail",
        "item": "Votre travail a-t-il du sens pour vous ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq43",
        "domaine": "Vécu professionnel", "categorie": "Sens du travail",
        "item": "Avez-vous le sentiment que le travail que vous faites est important ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq44",
        "domaine": "Vécu professionnel", "categorie": "Engagement",
        "item": "Recommanderiez-vous à un ami proche de postuler sur un emploi dans votre entreprise ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq45",
        "domaine": "Vécu professionnel", "categorie": "Engagement",
        "item": "Pensez-vous que votre entreprise est d'une grande importance pour vous ?",
        "reponses": ["Dans une très grande mesure", "Dans une grande mesure", "Plus ou moins", "Dans une faible mesure", "Dans une très faible mesure"],
        "scores": [100, 75, 50, 25, 0],
    },
    {
        "source": "copsoq", "code": "copsoq46",
        "domaine": "Vécu professionnel", "categorie": "Satisfaction",
        "item": "À quel point êtes-vous satisfait(e) de votre travail dans son ensemble ?",
        "reponses": ["Très satisfait(e)", "Satisfait(e)", "Insatisfait(e)", "Très insatisfait(e)"],
        "scores": [100, 66, 33, 0],  # 4 modalités uniquement
    },
]

QUESTIONS_WHOCOL = [
    # ---- Domaine : Environnement ----
    {
        "source": "whocol", "code": "8 (F16.1)",
        "domaine": "Environnement", "categorie": "Sécurité",
        "item": "Vous sentez vous en sécurité dans votre vie de tous les jours ?",
        "reponses": ["Pas du tout", "Un peu", "Modérément", "Beaucoup", "Tout à fait"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "whocol", "code": "9 (F22.1)",
        "domaine": "Environnement", "categorie": "Environnement physique",
        "item": "Votre environnement est-il sain (pollution, bruit, salubrité, etc.) ?",
        "reponses": ["Pas du tout", "Un peu", "Modérément", "Beaucoup", "Tout à fait"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "whocol", "code": "12 (F18.1)",
        "domaine": "Environnement", "categorie": "Ressources financières",
        "item": "Avez-vous assez d'argent pour satisfaire vos besoins ?",
        "reponses": ["Pas du tout", "Un peu", "Modérément", "Suffisamment", "Tout à fait"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "whocol", "code": "13 (F20.1)",
        "domaine": "Environnement", "categorie": "Information",
        "item": "Avez vous le sentiment d'être assez informé pour faire face à la vie de tous les jours ?",
        "reponses": ["Pas du tout", "Un peu", "Modérément", "Suffisamment", "Tout à fait"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "whocol", "code": "14 (F21.1)",
        "domaine": "Environnement", "categorie": "Loisirs",
        "item": "Avez-vous la possibilité d'avoir des activités de loisirs ?",
        "reponses": ["Pas du tout", "Un peu", "Modérément", "Suffisamment", "Tout à fait"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "whocol", "code": "23 (F17.3)",
        "domaine": "Environnement", "categorie": "Logement",
        "item": "Etes-vous satisfait de l'endroit où vous vivez ?",
        "reponses": ["Pas du tout satisfait", "Pas satisfait", "Ni satisfait ni insatisfait", "Satisfait", "Très satisfait"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "whocol", "code": "24 (F19.3)",
        "domaine": "Environnement", "categorie": "Soins de santé",
        "item": "Avez vous facilement accès aux soins dont vous avez besoin ?",
        "reponses": ["Pas du tout", "Un peu", "Modérément", "Beaucoup", "Tout à fait"],
        "scores": [0, 25, 50, 75, 100],
    },
    # ---- Domaine : Global ----
    {
        "source": "whocol", "code": "1 (G1)",
        "domaine": "Global", "categorie": "Qualité de vie",
        "item": "Comment trouvez-vous votre qualité de vie ?",
        "reponses": ["Très mauvaise", "Mauvaise", "Ni bonne, ni mauvaise", "Bonne", "Très bonne"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "whocol", "code": "2 (G4)",
        "domaine": "Global", "categorie": "Santé globale",
        "item": "Etes-vous satisfait de votre santé ?",
        "reponses": ["Pas du tout satisfait", "Pas satisfait", "Ni satisfait ni insatisfait", "Satisfait", "Très satisfait"],
        "scores": [0, 25, 50, 75, 100],
    },
    # ---- Domaine : Physique ----
    {
        "source": "whocol", "code": "3 (F1.4)",
        "domaine": "Physique", "categorie": "Douleur",
        "item": "La douleur (physique) vous empêche-t-elle de faire ce que vous avez à faire ?",
        "reponses": ["Pas du tout", "Un peu", "Modérément", "Beaucoup", "Complètement"],
        "scores": [100, 75, 50, 25, 0],  # Inversé : douleur = mauvais
    },
    {
        "source": "whocol", "code": "10 (F2.1)",
        "domaine": "Physique", "categorie": "Énergie",
        "item": "Avez-vous assez d'énergie dans la vie de tous les jours ?",
        "reponses": ["Pas du tout", "Un peu", "Modérément", "Suffisamment", "Tout à fait"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "whocol", "code": "16 (F3.3)",
        "domaine": "Physique", "categorie": "Sommeil",
        "item": "Etes-vous satisfait de votre sommeil ?",
        "reponses": ["Très insatisfait", "Insatisfait", "Ni satisfait ni insatisfait", "Satisfait", "Très satisfait"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "whocol", "code": "17 (F10.3)",
        "domaine": "Physique", "categorie": "Capacité fonctionnelle",
        "item": "Etes-vous satisfait de votre capacité à accomplir vos activités quotidiennes ?",
        "reponses": ["Très insatisfait", "Insatisfait", "Ni satisfait ni insatisfait", "Satisfait", "Très satisfait"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "whocol", "code": "18 (F12.4)",
        "domaine": "Physique", "categorie": "Capacité de travail",
        "item": "Etes-vous satisfait de votre capacité à travailler ?",
        "reponses": ["Très insatisfait", "Insatisfait", "Ni satisfait ni insatisfait", "Satisfait", "Très satisfait"],
        "scores": [0, 25, 50, 75, 100],
    },
    # ---- Domaine : Psychologie ----
    {
        "source": "whocol", "code": "5 (F4.1)",
        "domaine": "Psychologie", "categorie": "Plaisir de vivre",
        "item": "Trouvez-vous la vie agréable ?",
        "reponses": ["Pas du tout", "Un peu", "Modérément", "Beaucoup", "Complètement"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "whocol", "code": "6 (F24.2)",
        "domaine": "Psychologie", "categorie": "Spiritualité",
        "item": "Vos croyances personnelles donnent-elles un sens à votre vie ?",
        "reponses": ["Pas du tout", "Un peu", "Modérément", "Beaucoup", "Complètement"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "whocol", "code": "7 (5.3)",
        "domaine": "Psychologie", "categorie": "Concentration",
        "item": "Etes-vous capable de vous concentrer ?",
        "reponses": ["Pas du tout", "Un peu", "Modérément", "Beaucoup", "Tout à fait"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "whocol", "code": "19 (F6.3)",
        "domaine": "Psychologie", "categorie": "Estime de soi",
        "item": "Avez-vous une bonne opinion de vous-même ?",
        "reponses": ["Pas du tout", "Un peu", "Modérément", "Beaucoup", "Extrêmement"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "whocol", "code": "26 (F8.1)",
        "domaine": "Psychologie", "categorie": "Sentiments négatifs",
        "item": "Eprouvez-vous souvent des sentiments négatifs comme le cafard, le désespoir, l'anxiété ou la dépression ?",
        "reponses": ["Jamais", "Parfois", "Souvent", "Très souvent", "Toujours"],
        "scores": [0, 25, 50, 75, 100],  # Note : score bas = peu de sentiments négatifs = bon
    },
    # ---- Domaine : Relations sociales ----
    {
        "source": "whocol", "code": "20 (F13.3)",
        "domaine": "Relations sociales", "categorie": "Relations personnelles",
        "item": "Etes-vous satisfait de vos relations personnelles ?",
        "reponses": ["Pas du tout satisfait", "Pas satisfait", "Ni satisfait ni insatisfait", "Satisfait", "Très satisfait"],
        "scores": [0, 25, 50, 75, 100],
    },
    {
        "source": "whocol", "code": "22 (F14.4)",
        "domaine": "Relations sociales", "categorie": "Soutien social",
        "item": "Etes-vous satisfait du soutien que vous recevez de vos amis ?",
        "reponses": ["Pas du tout satisfait", "Pas satisfait", "Ni satisfait ni insatisfait", "Satisfait", "Très satisfait"],
        "scores": [0, 25, 50, 75, 100],
    },
]

# On regroupe tout pour faciliter l'import
TOUTES_LES_QUESTIONS = QUESTIONS_COPSOQ + QUESTIONS_WHOCOL

# Stats rapides (utiles pour les logs au démarrage)
NB_COPSOQ = len(QUESTIONS_COPSOQ)   # 46
NB_WHOCOL = len(QUESTIONS_WHOCOL)   # 22
NB_TOTAL  = len(TOUTES_LES_QUESTIONS)
