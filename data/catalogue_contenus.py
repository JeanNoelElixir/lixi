# ============================================================
# data/catalogue_contenus.py — Catalogue éditorial santé LIXIA
# ============================================================
# 27 contenus issus de la matrice Excel (colonne "Contenus"),
# un par thème identifié pour chacune des 10 familles.
#
# Structure de chaque contenu :
#   theme_code      → code famille (ex: "etat_emotionnel")
#   title           → titre affiché
#   ultra_short_text→ accroche de quelques mots (carte de recommandation)
#   short_text      → résumé 2-3 phrases (zone de restitution)
#   long_text       → article complet (clic "Lire plus")
#   display_order   → ordre d'affichage dans la famille (1 = prioritaire)
# ============================================================

CONTENUS = [

    # ══════════════════════════════════════════════════════
    # FAMILLE 1 — État émotionnel & humeur
    # ══════════════════════════════════════════════════════
    {
        "theme_code":       "etat_emotionnel",
        "title":            "Anxiété & régulation émotionnelle",
        "ultra_short_text": "Comprendre et apaiser l'anxiété",
        "short_text": (
            "L'anxiété est une réaction normale face à l'incertitude ou à la pression. "
            "Elle devient problématique quand elle s'installe dans la durée et perturbe "
            "le quotidien. Quelques techniques simples permettent de l'apprivoiser."
        ),
        "long_text": (
            "## Qu'est-ce que l'anxiété au travail ?\n\n"
            "L'anxiété est une tension intérieure liée à l'anticipation d'un danger ou d'une difficulté. "
            "Au travail, elle peut être déclenchée par une surcharge, une évaluation, un conflit ou "
            "simplement l'incertitude sur l'avenir. Ce n'est pas un signe de faiblesse — c'est un signal "
            "que quelque chose mérite attention.\n\n"
            "## 3 techniques rapides pour réguler\n\n"
            "**1. La respiration 4-7-8** : inspirez 4 secondes, retenez 7, expirez 8. "
            "Ce rythme active le système parasympathique et calme le corps en quelques cycles.\n\n"
            "**2. L'ancrage sensoriel** : nommez mentalement 5 choses que vous voyez, 4 que vous "
            "entendez, 3 que vous touchez. Cela ramène l'attention au présent.\n\n"
            "**3. L'écriture rapide** : notez en 2 minutes ce qui vous préoccupe, puis posez-vous "
            "la question : 'Qu'est-ce que je peux faire là, maintenant ?' Cette question déplace "
            "l'attention de la rumination vers l'action possible.\n\n"
            "## Quand consulter ?\n\n"
            "Si l'anxiété est intense, durable (plus de 2 semaines) ou qu'elle perturbe le sommeil "
            "et les relations, il est utile d'en parler à un professionnel de santé. "
            "Un coach ou un médecin du travail peut être une première étape simple."
        ),
        "display_order": 1,
    },
    {
        "theme_code":       "etat_emotionnel",
        "title":            "Fatigue émotionnelle : reconnaître les signaux",
        "ultra_short_text": "Quand les émotions épuisent",
        "short_text": (
            "La fatigue émotionnelle s'installe discrètement : irritabilité, cynisme, "
            "sentiment d'être à bout. La reconnaître tôt, c'est éviter qu'elle s'aggrave."
        ),
        "long_text": (
            "## Les signaux d'alerte\n\n"
            "La fatigue émotionnelle ne ressemble pas à la fatigue physique. Elle se manifeste par "
            "une irritabilité inhabituelle, une perte d'empathie, un sentiment de vide ou d'indifférence "
            "face à des situations qui vous touchaient avant. Le travail devient mécanique.\n\n"
            "## Pourquoi ça arrive ?\n\n"
            "Les métiers qui impliquent beaucoup d'interactions, de responsabilités ou d'empathie sont "
            "particulièrement concernés. On donne, on absorbe les émotions des autres, et les réserves "
            "se vident progressivement si on ne les recharge pas.\n\n"
            "## Ce qui aide\n\n"
            "**Mettre des limites claires** entre les moments de disponibilité et les moments de "
            "récupération. **Identifier une activité ressourçante** par jour, même courte (20 minutes "
            "de marche, un repas sans écran, une conversation légère). "
            "**Parler de ce qu'on vit** avec quelqu'un de confiance — nommer les émotions les "
            "allège souvent."
        ),
        "display_order": 2,
    },
    {
        "theme_code":       "etat_emotionnel",
        "title":            "Pause & souffle : s'accorder des micro-récupérations",
        "ultra_short_text": "Souffler pour mieux tenir",
        "short_text": (
            "On ne récupère pas seulement la nuit. Les micro-pauses pendant la journée "
            "sont essentielles pour maintenir l'équilibre émotionnel et la concentration."
        ),
        "long_text": (
            "## Le mythe de l'endurance continue\n\n"
            "Le cerveau n'est pas fait pour rester concentré et sous tension des heures d'affilée. "
            "Des études montrent qu'après 90 minutes d'effort cognitif, la performance chute et "
            "les erreurs augmentent. Les pauses ne sont pas du temps perdu — elles sont du temps "
            "investi dans la durée.\n\n"
            "## Comment faire des vraies pauses ?\n\n"
            "Une vraie pause, c'est une coupure complète : pas d'email, pas de téléphone. "
            "Idéalement, un changement de posture (se lever), un changement d'environnement "
            "(sortir du bureau) et un changement d'activité (marcher, s'étirer, boire lentement).\n\n"
            "**La règle des 52/17** : 52 minutes de concentration, 17 minutes de vraie pause. "
            "Ce rythme, identifié par des chercheurs, est celui des personnes les plus productives.\n\n"
            "## La pause comme signal de respect de soi\n\n"
            "S'accorder une pause, c'est aussi reconnaître qu'on a des limites et qu'on les respecte. "
            "C'est un geste de régulation, pas un aveu de faiblesse."
        ),
        "display_order": 3,
    },

    # ══════════════════════════════════════════════════════
    # FAMILLE 2 — Fatigue & récupération
    # ══════════════════════════════════════════════════════
    {
        "theme_code":       "fatigue_recuperation",
        "title":            "Fatigue accumulée : comprendre la dette de sommeil",
        "ultra_short_text": "Quand la fatigue s'accumule",
        "short_text": (
            "La fatigue accumulée ne se règle pas avec une nuit de rattrapage. "
            "Elle s'installe progressivement et nécessite une récupération structurée."
        ),
        "long_text": (
            "## La dette de sommeil, c'est quoi ?\n\n"
            "Chaque nuit incomplète crée un déficit que le corps tente de compenser. "
            "Après plusieurs semaines de sommeil insuffisant, ce déficit s'accumule et affecte "
            "la mémoire, la prise de décision, la régulation émotionnelle et le système immunitaire.\n\n"
            "## Les signes que la fatigue est profonde\n\n"
            "Au-delà du manque d'énergie habituel : difficulté à démarrer le matin même après "
            "8 heures de sommeil, besoin impérieux de sieste en journée, sensation de 'marcher "
            "dans le brouillard', irritabilité disproportionnée aux situations.\n\n"
            "## Comment récupérer vraiment ?\n\n"
            "La récupération profonde demande du temps et de la régularité. "
            "**Couper l'exposition aux écrans 1h avant de dormir** (la lumière bleue retarde "
            "la mélatonine). **Maintenir des horaires de lever stables**, même le week-end. "
            "**Introduire des plages de repos actif** dans la semaine : nature, lecture, activité "
            "physique douce. Une courte sieste de 20 minutes en milieu de journée peut compenser "
            "un déficit sans perturber le sommeil nocturne."
        ),
        "display_order": 1,
    },
    {
        "theme_code":       "fatigue_recuperation",
        "title":            "Récupération active : les bonnes pratiques",
        "ultra_short_text": "Récupérer autrement que dormir",
        "short_text": (
            "Récupérer ne signifie pas seulement dormir. L'activité physique légère, "
            "la déconnexion numérique et les activités agréables rechargent les batteries "
            "différemment — et souvent plus vite."
        ),
        "long_text": (
            "## Pourquoi le repos passif ne suffit pas ?\n\n"
            "Rester immobile devant un écran ou scroller sur son téléphone après le travail "
            "n'est pas vraiment du repos. Le cerveau continue de traiter des informations, "
            "souvent négatives, sans que le corps se régénère.\n\n"
            "## Les piliers de la récupération active\n\n"
            "**L'activité physique** : même 20-30 minutes de marche rapide réduisent le cortisol "
            "(hormone du stress) et libèrent des endorphines. Ce n'est pas une question de performance "
            "sportive — c'est de la physiologie.\n\n"
            "**La déconnexion numérique** : définir des plages sans téléphone, notamment les "
            "2 premières heures du matin et la dernière heure avant le coucher.\n\n"
            "**Les activités à flux** : toute activité qui absorbe complètement l'attention "
            "(cuisine, musique, jardinage, jeu) met le cerveau 'en veille' et recharge les "
            "ressources cognitives.\n\n"
            "**Le contact social choisi** : passer du temps avec des personnes qui donnent "
            "de l'énergie plutôt qu'elles n'en prennent."
        ),
        "display_order": 2,
    },
    {
        "theme_code":       "fatigue_recuperation",
        "title":            "Signaux d'usure : quand le corps parle",
        "ultra_short_text": "Les signaux à ne pas ignorer",
        "short_text": (
            "Maux de tête fréquents, tensions musculaires, digestion perturbée... "
            "Le corps exprime souvent ce que l'esprit minimise. Ces signaux méritent attention."
        ),
        "long_text": (
            "## Le corps comme baromètre\n\n"
            "Le stress chronique et la fatigue se manifestent d'abord physiquement : tensions "
            "dans la nuque et les épaules, maux de tête, troubles du sommeil, fatigue digestive, "
            "infections répétées. Ces symptômes sont souvent minimisés ou attribués à autre chose.\n\n"
            "## Comprendre le lien corps-esprit\n\n"
            "Le système nerveux autonome régule à la fois nos émotions et nos fonctions corporelles. "
            "Quand il est en état d'alerte prolongé, il mobilise des ressources au détriment de la "
            "récupération, de la digestion et du système immunitaire. Ce n'est pas 'dans la tête' — "
            "c'est de la biologie.\n\n"
            "## Ce qu'on peut faire\n\n"
            "**Tenir un journal des symptômes** sur 2 semaines pour identifier les patterns "
            "(le lundi matin ? avant certaines réunions ?). **Consulter un médecin** si les symptômes "
            "persistent — certains signaux nécessitent un bilan. **Intégrer des pratiques corporelles** "
            "simples : respiration, étirements, marche — qui activent le système parasympathique."
        ),
        "display_order": 3,
    },

    # ══════════════════════════════════════════════════════
    # FAMILLE 3 — Charge mentale & cognition
    # ══════════════════════════════════════════════════════
    {
        "theme_code":       "charge_mentale",
        "title":            "Charge mentale : quand la tête est trop pleine",
        "ultra_short_text": "Alléger la charge invisible",
        "short_text": (
            "La charge mentale, c'est tout ce qu'on porte en tête sans pouvoir le poser : "
            "les tâches non terminées, les décisions en suspens, les responsabilités implicites. "
            "Elle épuise même quand on ne fait 'rien'."
        ),
        "long_text": (
            "## Qu'est-ce que la charge mentale ?\n\n"
            "La charge mentale désigne l'ensemble des tâches cognitives invisibles : anticiper, "
            "planifier, mémoriser, coordonner, prendre des décisions. Elle ne se voit pas, mais "
            "elle consomme en permanence de la bande passante mentale.\n\n"
            "## Pourquoi elle épuise plus que le travail visible ?\n\n"
            "Le cerveau en mode 'charge mentale élevée' reste en état d'activation même au repos. "
            "On pense au travail le soir, on se réveille la nuit avec une idée, on n'arrive pas "
            "à vraiment déconnecter. C'est un état de vigilance continue qui vide les ressources.\n\n"
            "## Des leviers concrets\n\n"
            "**Externaliser** : écrire tout ce qui est en tête dans un système de capture "
            "(carnet, appli) libère la mémoire de travail. Le cerveau lâche ce qu'il sait "
            "être écrit quelque part.\n\n"
            "**Prioriser avec méthode** : la matrice urgent/important (Eisenhower) aide à "
            "distinguer ce qui compte vraiment de ce qui est juste bruyant.\n\n"
            "**Délimiter des plages de non-interruption** : les interruptions multiplient la "
            "charge mentale. Chaque tâche interrompue coûte en moyenne 23 minutes pour "
            "retrouver le fil."
        ),
        "display_order": 1,
    },
    {
        "theme_code":       "charge_mentale",
        "title":            "Stress nocif : quand la pression dépasse les ressources",
        "ultra_short_text": "Comprendre le bon et le mauvais stress",
        "short_text": (
            "Tout stress n'est pas néfaste. Le stress aigu peut être mobilisateur. "
            "C'est le stress chronique — quand la pression dure sans relâche — qui abîme."
        ),
        "long_text": (
            "## Le bon et le mauvais stress\n\n"
            "Le stress est une réponse d'adaptation : il mobilise l'énergie, aiguise la vigilance "
            "et prépare à l'action. À court terme, c'est un atout. Le problème, c'est quand "
            "le système d'alarme reste enclenché en permanence, sans phase de récupération.\n\n"
            "## Ce que le stress chronique fait au corps et au cerveau\n\n"
            "Le cortisol, hormone du stress, en excès prolongé altère la mémoire, réduit la "
            "capacité de concentration, perturbe le sommeil et affaiblit le système immunitaire. "
            "Il diminue aussi la créativité et la capacité à voir des solutions nouvelles.\n\n"
            "## Identifier ses déclencheurs\n\n"
            "Chaque personne a ses propres déclencheurs de stress. Les identifier permet de "
            "mieux les anticiper. Une technique simple : noter pendant une semaine les moments "
            "où le stress monte, en précisant la situation, la pensée associée et la sensation "
            "physique. Des patterns émergent rapidement.\n\n"
            "## Agir sur ce qu'on peut\n\n"
            "On ne peut pas toujours changer les sources de stress, mais on peut agir sur "
            "sa relation à ces sources. La pleine conscience, l'exercice physique régulier et "
            "le soutien social sont les trois leviers les mieux documentés scientifiquement."
        ),
        "display_order": 2,
    },
    {
        "theme_code":       "charge_mentale",
        "title":            "Délestage & priorisation : faire moins pour faire mieux",
        "ultra_short_text": "L'art de décider quoi lâcher",
        "short_text": (
            "Face à la surcharge, la solution n'est pas de faire plus vite ou plus longtemps. "
            "C'est d'identifier ce qui peut être délégué, différé ou supprimé."
        ),
        "long_text": (
            "## Pourquoi 'tout faire' est une illusion\n\n"
            "L'attention est une ressource limitée et non renouvelable à la journée. "
            "Croire qu'on peut tout traiter avec la même qualité est une illusion qui conduit "
            "à la médiocrité généralisée plutôt qu'à l'excellence ciblée.\n\n"
            "## La matrice d'Eisenhower\n\n"
            "Classez vos tâches selon deux axes : urgent vs non urgent, et important vs non important.\n\n"
            "- **Urgent + Important** : faites-le maintenant\n"
            "- **Important + Non urgent** : planifiez-le (c'est souvent là que se trouve la valeur réelle)\n"
            "- **Urgent + Non important** : déléguez si possible\n"
            "- **Non urgent + Non important** : éliminez\n\n"
            "## Le 'non' comme outil de performance\n\n"
            "Dire non à une demande secondaire, c'est dire oui à ce qui compte vraiment. "
            "Savoir refuser avec tact ('Je ne peux pas cette semaine, mais je pourrais la semaine "
            "prochaine') est une compétence qui se travaille et se renforce avec la pratique."
        ),
        "display_order": 3,
    },

    # ══════════════════════════════════════════════════════
    # FAMILLE 4 — Santé sociale & soutien
    # ══════════════════════════════════════════════════════
    {
        "theme_code":       "sante_sociale",
        "title":            "Isolement & soutien : briser la solitude au travail",
        "ultra_short_text": "Se sentir moins seul au travail",
        "short_text": (
            "L'isolement au travail — même entouré de collègues — est un facteur de risque "
            "majeur. Le sentiment de ne pas être soutenu pèse autant que la charge de travail."
        ),
        "long_text": (
            "## L'isolement invisible\n\n"
            "On peut se sentir profondément seul dans un open space plein de monde. "
            "L'isolement au travail, ce n'est pas l'absence physique de collègues — c'est "
            "le sentiment de ne pas être compris, de ne pas pouvoir parler de ce qu'on vit "
            "vraiment, de ne pas compter pour les autres.\n\n"
            "## Pourquoi le soutien social est protecteur\n\n"
            "Le soutien social est l'un des facteurs de résilience les mieux documentés. "
            "Avoir quelqu'un à qui parler, qui comprend notre contexte, qui peut offrir un "
            "regard extérieur ou simplement écouter, réduit significativement l'impact "
            "du stress sur la santé.\n\n"
            "## Comment recréer du lien quand on s'est replié\n\n"
            "L'isolement crée un cercle : plus on se replie, plus ça devient difficile d'aller "
            "vers les autres. Des petits gestes brisent ce cercle : initier une pause café, "
            "poser une question à un collègue, partager un retour positif. "
            "Ce ne sont pas des grands discours — c'est l'accumulation de petits gestes qui "
            "crée la texture du lien."
        ),
        "display_order": 1,
    },
    {
        "theme_code":       "sante_sociale",
        "title":            "Relations de travail : gérer les tensions",
        "ultra_short_text": "Désamorcer les conflits relationnels",
        "short_text": (
            "Les relations difficiles au travail sont une source majeure de mal-être. "
            "Elles ne se règlent pas en les ignorant — mais avec des outils simples, "
            "beaucoup de tensions peuvent être désamorcées."
        ),
        "long_text": (
            "## Pourquoi les conflits s'enlisent\n\n"
            "La plupart des conflits au travail ne viennent pas de personnes mal intentionnées, "
            "mais de malentendus, de besoins non exprimés ou de perceptions divergentes. "
            "Ce qu'on interprète comme une attaque est souvent une maladresse ou une différence "
            "de style de communication.\n\n"
            "## La communication non-violente (CNV)\n\n"
            "La CNV propose 4 étapes pour exprimer une tension sans attaquer :\n\n"
            "1. **Observation** : 'Quand tu coupes la parole en réunion...'\n"
            "2. **Sentiment** : '...je me sens peu considéré(e)...'\n"
            "3. **Besoin** : '...car j'ai besoin de pouvoir finir ma pensée...'\n"
            "4. **Demande** : '...est-ce que tu pourrais me laisser terminer avant d'intervenir ?'\n\n"
            "Cette formulation évite l'accusation et ouvre un espace de dialogue.\n\n"
            "## Quand escalader ?\n\n"
            "Si la tension est récurrente, intense ou qu'elle impacte le travail de l'équipe, "
            "impliquer un tiers (manager, RH, médiateur) n'est pas une défaite — c'est une "
            "décision professionnelle mature."
        ),
        "display_order": 2,
    },
    {
        "theme_code":       "sante_sociale",
        "title":            "Oser en parler : demander de l'aide sans honte",
        "ultra_short_text": "Demander de l'aide, c'est courageux",
        "short_text": (
            "Dans beaucoup d'environnements professionnels, demander de l'aide est perçu "
            "comme un aveu de faiblesse. C'est l'inverse : c'est un signe d'intelligence situationnelle."
        ),
        "long_text": (
            "## Le mythe de l'autonomie totale\n\n"
            "L'idéal du professionnel qui 'gère tout seul' est une fiction coûteuse. "
            "Les meilleurs performers, dans tous les domaines, ont des mentors, des coachs, "
            "des pairs à qui ils parlent de leurs difficultés. La vulnérabilité partagée "
            "crée de la confiance et accélère les apprentissages.\n\n"
            "## Ce qui empêche de demander de l'aide\n\n"
            "La peur du jugement ('ils vont penser que je ne suis pas capable'), "
            "la honte ('ça fait longtemps que j'aurais dû régler ça'), "
            "le perfectionnisme ('je dois d'abord avoir tout essayé'). "
            "Ces freins sont compréhensibles — mais ils coûtent souvent plus cher "
            "que la situation elle-même.\n\n"
            "## Comment demander efficacement\n\n"
            "**Être précis** : 'J'ai du mal avec X, est-ce que tu as 15 minutes pour m'aider ?' "
            "fonctionne mieux que 'J'y arrive pas'. "
            "**Choisir le bon interlocuteur** : quelqu'un qui a vécu quelque chose de similaire "
            "ou qui a des ressources que vous n'avez pas. "
            "**Accepter que l'aide prenne des formes inattendues** : parfois, ce n'est pas "
            "une solution qu'on reçoit, mais un regard différent — et ça suffit."
        ),
        "display_order": 3,
    },

    # ══════════════════════════════════════════════════════
    # FAMILLE 5 — Exigences & pression au travail
    # ══════════════════════════════════════════════════════
    {
        "theme_code":       "exigences_pression",
        "title":            "Surcharge au travail : quand trop c'est trop",
        "ultra_short_text": "Reconnaître et nommer la surcharge",
        "short_text": (
            "La surcharge de travail n'est pas une question de motivation ou de compétence. "
            "C'est un déséquilibre objectif entre les ressources disponibles et les exigences. "
            "La nommer est déjà un premier pas."
        ),
        "long_text": (
            "## Ce que la surcharge fait vraiment\n\n"
            "Face à une charge excessive, le cerveau entre en mode survie : il priorise "
            "l'urgent sur l'important, réduit la créativité, augmente les erreurs et "
            "l'irritabilité. Ce n'est pas un manque de volonté — c'est de la biologie.\n\n"
            "## La différence entre charge réelle et charge perçue\n\n"
            "Parfois la charge est objectivement excessive. Parfois elle est amplifiée "
            "par le perfectionnisme, la difficulté à déléguer ou la peur de décevoir. "
            "Distinguer les deux aide à trouver les bons leviers.\n\n"
            "## Agir à trois niveaux\n\n"
            "**Sur soi** : identifier ce qu'on peut lâcher sans conséquence réelle. "
            "Souvent, 20% des tâches produisent 80% de la valeur.\n\n"
            "**Avec son manager** : exprimer la surcharge avec des faits ('je gère X dossiers "
            "simultanément, voilà ce que je peux prioriser cette semaine') plutôt qu'avec "
            "des émotions seules.\n\n"
            "**Dans l'organisation** : certaines surcharges nécessitent des ajustements "
            "structurels — effectifs, processus, outils. Ce n'est pas tabou d'en parler."
        ),
        "display_order": 1,
    },
    {
        "theme_code":       "exigences_pression",
        "title":            "Surchauffe : les signaux qui précèdent le burnout",
        "ultra_short_text": "Repérer la surchauffe avant qu'il soit trop tard",
        "short_text": (
            "Le burnout ne surgit pas d'un coup. Il s'installe progressivement sur des mois. "
            "Reconnaître les signaux précoces permet d'agir avant d'atteindre l'épuisement total."
        ),
        "long_text": (
            "## Le burnout : un processus, pas un événement\n\n"
            "L'épuisement professionnel (burnout) est défini par trois dimensions : "
            "épuisement émotionnel, cynisme/dépersonnalisation envers le travail, "
            "et sentiment de perte d'efficacité. Il s'installe sur des semaines ou des mois, "
            "souvent chez des personnes très engagées qui 'tiennent' jusqu'à ne plus pouvoir.\n\n"
            "## Les signaux précoces à surveiller\n\n"
            "**Physiques** : fatigue persistante qui ne passe pas avec le repos, maux "
            "de tête fréquents, troubles du sommeil.\n\n"
            "**Émotionnels** : irritabilité croissante, sentiment d'être 'vide', "
            "perte de plaisir dans des activités qui aimaient.\n\n"
            "**Comportementaux** : augmentation du temps de travail sans gain de productivité, "
            "isolement social, cynisme inhabituel sur le travail ou les collègues.\n\n"
            "**Cognitifs** : difficultés de concentration, oublis inhabituels, "
            "sentiment de ne plus avoir de ressources créatives.\n\n"
            "## Si vous vous reconnaissez\n\n"
            "Parlez-en à votre médecin traitant. Le burnout est une condition médicalement "
            "reconnue qui nécessite souvent un arrêt et un accompagnement. "
            "Attendre ne fait qu'aggraver les choses."
        ),
        "display_order": 2,
    },
    {
        "theme_code":       "exigences_pression",
        "title":            "Prévention du burnout : construire des amortisseurs",
        "ultra_short_text": "Construire sa résilience au quotidien",
        "short_text": (
            "La prévention du burnout ne passe pas par l'élimination du stress — "
            "impossible — mais par la construction de ressources qui absorbent ce stress "
            "sur le long terme."
        ),
        "long_text": (
            "## Les ressources protectrices\n\n"
            "La recherche sur la résilience au travail identifie plusieurs ressources qui "
            "agissent comme amortisseurs face aux exigences :\n\n"
            "**L'autonomie** : avoir une marge de manœuvre sur comment on fait son travail "
            "réduit significativement l'impact des exigences.\n\n"
            "**Le soutien social** : avoir des collègues et un manager sur qui compter "
            "multiplie la capacité à absorber la pression.\n\n"
            "**Le sens** : comprendre pourquoi son travail compte — pour l'équipe, pour "
            "les clients, pour la société — permet de mobiliser des ressources supplémentaires "
            "dans les moments difficiles.\n\n"
            "**La récupération** : des rituels de déconnexion réguliers et efficaces "
            "(pas des week-ends entiers à culpabiliser de ne pas travailler).\n\n"
            "## Ce que vous pouvez faire dès aujourd'hui\n\n"
            "Identifiez une ressource que vous pouvez renforcer cette semaine. "
            "Pas tout à la fois — une chose concrète, faisable, qui peut changer quelque chose."
        ),
        "display_order": 3,
    },

    # ══════════════════════════════════════════════════════
    # FAMILLE 6 — Autonomie & contrôle
    # ══════════════════════════════════════════════════════
    {
        "theme_code":       "autonomie_controle",
        "title":            "Reprendre du contrôle : agir là où c'est possible",
        "ultra_short_text": "Retrouver de la maîtrise",
        "short_text": (
            "Le sentiment de perte de contrôle est l'un des facteurs de stress les plus "
            "puissants. Identifier ce sur quoi on peut agir — même à petite échelle — "
            "rétablit un sentiment d'efficacité essentiel."
        ),
        "long_text": (
            "## Le cercle de contrôle\n\n"
            "Stephen Covey distinguait le 'cercle d'influence' (ce sur quoi on peut agir) "
            "du 'cercle de préoccupation' (ce qui nous préoccupe mais qu'on ne contrôle pas). "
            "L'énergie investie dans le cercle de préoccupation épuise sans résultat. "
            "Celle investie dans le cercle d'influence produit des changements réels.\n\n"
            "## Identifier ses marges de manœuvre\n\n"
            "Même dans des contextes très contraints, il existe souvent des espaces d'action : "
            "comment on organise sa journée, avec qui on interagit en premier, quels projets "
            "on choisit de prioriser, comment on communique. Ces petits choix, accumulés, "
            "redonnent un sentiment d'agence.\n\n"
            "## Quand l'environnement ne change pas\n\n"
            "Si les contraintes sont réelles et durables, la question devient : "
            "'Est-ce que je peux m'adapter à cet environnement, ou est-il temps d'en changer ?' "
            "Cette question, posée lucidement, est légitime et utile."
        ),
        "display_order": 1,
    },
    {
        "theme_code":       "autonomie_controle",
        "title":            "Marges de manœuvre : négocier son espace de travail",
        "ultra_short_text": "Négocier son autonomie",
        "short_text": (
            "L'autonomie au travail ne se décrète pas — elle se négocie et se construit "
            "progressivement. Comprendre comment l'élargir dans son contexte spécifique "
            "est une compétence professionnelle précieuse."
        ),
        "long_text": (
            "## Pourquoi l'autonomie compte autant\n\n"
            "Les études sur la motivation au travail (notamment celles de Deci et Ryan sur "
            "l'autodétermination) montrent que l'autonomie est un besoin psychologique "
            "fondamental. Quand il est satisfait, l'engagement, la créativité et la "
            "satisfaction augmentent. Quand il est frustré, le désengagement s'installe.\n\n"
            "## Comment négocier plus d'espace\n\n"
            "**Commencer par démontrer la fiabilité** : l'autonomie s'accorde plus facilement "
            "quand la confiance est établie. Tenir ses engagements, communiquer proactivement "
            "sur les avancées crée les conditions de l'autonomie.\n\n"
            "**Formuler des propositions concrètes** : 'Je voudrais essayer de gérer ce projet "
            "de façon plus autonome — voilà comment je m'organiserais et comment je vous "
            "rendrais compte' est plus efficace que 'j'aimerais plus de liberté'.\n\n"
            "**Identifier les espaces déjà disponibles** : parfois l'autonomie existe mais "
            "n'est pas utilisée par habitude ou par peur de dépasser les limites."
        ),
        "display_order": 2,
    },

    # ══════════════════════════════════════════════════════
    # FAMILLE 7 — Clarté & organisation
    # ══════════════════════════════════════════════════════
    {
        "theme_code":       "clarte_organisation",
        "title":            "Rôles flous & repères : clarifier les attentes",
        "ultra_short_text": "Clarifier qui fait quoi",
        "short_text": (
            "Le flou dans les rôles et les attentes est une source de stress souvent "
            "sous-estimée. On peut travailler beaucoup sans savoir si on travaille juste. "
            "Clarifier les attentes est un geste de performance et de santé."
        ),
        "long_text": (
            "## Le coût du flou\n\n"
            "Quand les rôles, les responsabilités ou les critères de succès ne sont pas clairs, "
            "le cerveau comble le vide par des suppositions — souvent anxiogènes. "
            "On sur-travaille par peur de ne pas en faire assez, ou on évite certaines décisions "
            "par peur de dépasser son périmètre.\n\n"
            "## Comment clarifier les attentes\n\n"
            "**Demander explicitement** : 'Pour ce projet, quels sont pour toi les 3 critères "
            "principaux de succès ?' Cette question simple, posée à son manager, peut éviter "
            "des semaines de malentendu.\n\n"
            "**Reformuler pour valider** : après un brief, reformuler ce qu'on a compris "
            "et demander confirmation. 'Je comprends que ma priorité est X — c'est bien ça ?'\n\n"
            "**Documenter les accords** : même informellement, noter ce qui a été convenu "
            "crée une référence commune et évite les réinterprétations.\n\n"
            "## Et si les attentes sont contradictoires ?\n\n"
            "Mettre à plat les contradictions explicitement ('Tu me demandes à la fois X et Y — "
            "quand ils entrent en conflit, lequel je priorise ?') est plus efficace "
            "que de naviguer dans l'ambiguïté en silence."
        ),
        "display_order": 1,
    },
    {
        "theme_code":       "clarte_organisation",
        "title":            "Clarifier ses priorités : choisir plutôt que subir",
        "ultra_short_text": "Reprendre la main sur ses priorités",
        "short_text": (
            "Quand tout est urgent, rien ne l'est vraiment. Reprendre la main sur ses "
            "priorités — en les choisissant plutôt qu'en les subissant — change profondément "
            "le rapport au travail."
        ),
        "long_text": (
            "## Le piège de l'urgence permanente\n\n"
            "Dans un environnement où tout est 'prioritaire', l'attention se fragmente, "
            "la qualité baisse et le sentiment d'efficacité disparaît. On finit des journées "
            "épuisé sans avoir avancé sur ce qui comptait vraiment.\n\n"
            "## Reprendre la main : quelques méthodes\n\n"
            "**La règle du MIT** (Most Important Task) : chaque matin, avant d'ouvrir les emails, "
            "identifier la tâche la plus importante de la journée et la traiter en premier, "
            "pendant les 60-90 premières minutes.\n\n"
            "**Le time-blocking** : bloquer des créneaux dans l'agenda pour le travail de fond, "
            "comme on le ferait pour une réunion. Ce qui n'est pas bloqué est envahi.\n\n"
            "**La revue hebdomadaire** : 30 minutes chaque vendredi pour faire le bilan de la "
            "semaine et préparer la suivante. Ce rituel simple crée une continuité et réduit "
            "l'anxiété du lundi matin.\n\n"
            "## Communiquer ses priorités\n\n"
            "Partager ses priorités avec son manager ('voici ce sur quoi je me concentre cette "
            "semaine') évite les réorientations de dernière minute et crée un espace de "
            "dialogue sur ce qui compte vraiment."
        ),
        "display_order": 2,
    },

    # ══════════════════════════════════════════════════════
    # FAMILLE 8 — Management & reconnaissance
    # ══════════════════════════════════════════════════════
    {
        "theme_code":       "management_reconnaissance",
        "title":            "Reconnaissance & équité : se sentir compté",
        "ultra_short_text": "Le besoin fondamental de reconnaissance",
        "short_text": (
            "La reconnaissance au travail est un besoin humain fondamental. "
            "Son absence — plus que les conditions matérielles — est souvent au cœur "
            "des désengagements et des mal-être professionnels."
        ),
        "long_text": (
            "## Pourquoi la reconnaissance compte autant\n\n"
            "La reconnaissance n'est pas un luxe managérial — c'est un besoin de base "
            "lié à l'appartenance et à l'identité. Quand on se sent invisible ou "
            "injustement traité, la motivation s'érode, même si le salaire est bon "
            "et les conditions correctes.\n\n"
            "## Les différentes formes de reconnaissance\n\n"
            "**De la personne** : être vu comme un individu, pas seulement comme une fonction.\n\n"
            "**Des résultats** : que les succès soient remarqués et nommés.\n\n"
            "**De l'effort** : que l'engagement soit visible même quand le résultat n'est pas parfait.\n\n"
            "**Des compétences** : que l'expertise soit sollicitée et valorisée.\n\n"
            "## Ce qu'on peut faire quand la reconnaissance manque\n\n"
            "**Exprimer son besoin** : 'J'aurais besoin de savoir si mon travail sur ce projet "
            "a répondu aux attentes' est une demande légitime. "
            "**Chercher la reconnaissance ailleurs** : pairs, clients, communauté professionnelle. "
            "**S'auto-reconnaître** : tenir un journal de ce qu'on a accompli, même petits pas. "
            "C'est moins satisfaisant que la reconnaissance externe — mais ça tient."
        ),
        "display_order": 1,
    },
    {
        "theme_code":       "management_reconnaissance",
        "title":            "Relation hiérarchique : naviguer avec son manager",
        "ultra_short_text": "Construire une relation managériale saine",
        "short_text": (
            "La relation avec son manager est l'un des déterminants les plus puissants "
            "du bien-être au travail. Elle ne dépend pas uniquement du manager — "
            "on peut agir sur sa moitié."
        ),
        "long_text": (
            "## La relation managériale n'est pas un destin\n\n"
            "On entend souvent 'on quitte un manager, pas une entreprise'. C'est souvent vrai — "
            "mais la relation managériale est une relation, et comme toute relation, "
            "elle implique deux parties. On a plus d'influence qu'on ne le croit.\n\n"
            "## Ce qui fait une bonne relation manager-collaborateur\n\n"
            "**La clarté des attentes** (des deux côtés). **La confiance** qui se construit "
            "par la fiabilité et la transparence. **La communication proactive** : ne pas "
            "attendre l'entretien annuel pour faire le point. **La capacité à gérer les "
            "désaccords** de façon directe et respectueuse.\n\n"
            "## Améliorer une relation difficile\n\n"
            "**Comprendre le point de vue du manager** : quelles sont ses contraintes, "
            "ses priorités, ses pressions ? Cette compréhension change souvent la lecture "
            "de comportements perçus comme arbitraires.\n\n"
            "**Exprimer ce qui ne va pas** de façon factuelle et constructive : "
            "'Quand X se passe, je me sens Y, et j'aurais besoin de Z'.\n\n"
            "**Savoir escalader** si la relation est toxique ou si elle nuit durablement "
            "à la santé : RH, médecine du travail, manager du manager."
        ),
        "display_order": 2,
    },

    # ══════════════════════════════════════════════════════
    # FAMILLE 9 — Sens, motivation & satisfaction
    # ══════════════════════════════════════════════════════
    {
        "theme_code":       "sens_motivation",
        "title":            "Perte de sens : quand le travail sonne creux",
        "ultra_short_text": "Retrouver du sens dans son travail",
        "short_text": (
            "La perte de sens est une des formes les plus sournoises de souffrance au travail. "
            "On fait les gestes sans y croire. Comprendre d'où ça vient est le premier pas "
            "pour retrouver de la direction."
        ),
        "long_text": (
            "## La perte de sens : de quoi parle-t-on ?\n\n"
            "Le sens au travail, c'est le sentiment que ce qu'on fait compte — "
            "pour soi, pour les autres, pour quelque chose de plus grand. "
            "Quand ce sentiment disparaît, le travail devient une série de tâches "
            "déconnectées les unes des autres, et la motivation s'effondre.\n\n"
            "## Les causes fréquentes\n\n"
            "**Le décalage entre valeurs et pratiques** : quand ce qu'on fait contredit "
            "ce en quoi on croit.\n\n"
            "**L'absence de vision** : ne pas savoir où va l'organisation, ni comment "
            "son travail y contribue.\n\n"
            "**L'invisibilité de l'impact** : faire un travail dont on ne voit jamais "
            "les effets sur les personnes ou les situations qu'on est censé servir.\n\n"
            "**L'épuisement** : la fatigue empêche de percevoir le sens même quand il existe.\n\n"
            "## Retrouver du sens\n\n"
            "**Revenir à ses valeurs** : qu'est-ce qui comptait pour moi dans ce travail "
            "au début ? Est-ce encore accessible quelque part ?\n\n"
            "**Chercher l'impact direct** : rencontrer les personnes pour qui on travaille, "
            "voir les résultats concrets, lire des retours. Le sens se nourrit du concret.\n\n"
            "**Explorer** : parfois la perte de sens signale qu'une évolution est nécessaire — "
            "de poste, de missions, voire de direction professionnelle."
        ),
        "display_order": 1,
    },
    {
        "theme_code":       "sens_motivation",
        "title":            "Motivation & engagement : relancer la machine",
        "ultra_short_text": "Réamorcer sa motivation",
        "short_text": (
            "La motivation n'est pas un état fixe qu'on a ou qu'on n'a pas. "
            "C'est un processus dynamique qu'on peut influencer avec les bons leviers, "
            "même dans des contextes difficiles."
        ),
        "long_text": (
            "## La motivation intrinsèque et extrinsèque\n\n"
            "Les recherches en psychologie distinguent deux types de motivation. "
            "**Extrinsèque** : on fait quelque chose pour obtenir une récompense ou éviter "
            "une punition (salaire, reconnaissance, crainte du jugement). "
            "**Intrinsèque** : on fait quelque chose parce que l'activité elle-même est "
            "satisfaisante, stimulante ou alignée avec ses valeurs.\n\n"
            "La motivation intrinsèque est plus durable et plus résistante aux obstacles. "
            "Elle se cultive.\n\n"
            "## Comment réamorcer\n\n"
            "**Identifier ce qui était motivant avant** et chercher à en retrouver des traces "
            "dans le travail actuel. Même dans un contexte difficile, il y a souvent des "
            "îlots de sens.\n\n"
            "**Se fixer de petits défis** : la progression — apprendre quelque chose, "
            "maîtriser une compétence — est une source puissante de motivation intrinsèque.\n\n"
            "**Célébrer les petites victoires** : notre cerveau a un biais vers le négatif. "
            "Prendre conscience de ce qu'on accomplit, même modestement, rééquilibre.\n\n"
            "**Réduire ce qui vide** : identifier et limiter les tâches, interactions ou "
            "contextes qui épuisent sans apporter rien en retour."
        ),
        "display_order": 2,
    },
    {
        "theme_code":       "sens_motivation",
        "title":            "Réalignement : faire le point et décider",
        "ultra_short_text": "Se réaligner avec ce qui compte",
        "short_text": (
            "Parfois, le malaise au travail est un signal que quelque chose de plus profond "
            "mérite attention. Un moment de réalignement — faire le point sur ce qu'on veut "
            "vraiment — peut ouvrir des perspectives inattendues."
        ),
        "long_text": (
            "## Quand le malaise est un signal\n\n"
            "Il y a une différence entre une période difficile (passagère, contextuelle) "
            "et un décalage profond entre ce qu'on fait et ce qu'on est. "
            "Le premier se gère avec des ajustements. Le second appelle un réalignement.\n\n"
            "## Les questions utiles\n\n"
            "**Ce qui donne de l'énergie** : quelles sont les tâches, missions ou interactions "
            "dans lesquelles le temps passe vite et après lesquelles on se sent bien ?\n\n"
            "**Ce qui en prend** : à l'inverse, qu'est-ce qui épuise systématiquement ?\n\n"
            "**Ce qui compte** : si tout était possible, quelle version de sa vie professionnelle "
            "on choisirait ?\n\n"
            "**Ce qui manque** : autonomie, relation, impact, apprentissage, reconnaissance ?\n\n"
            "## Le réalignement ne nécessite pas toujours un grand changement\n\n"
            "Parfois c'est un ajustement de poste, de missions, de style de travail. "
            "Parfois c'est une conversation avec son manager. "
            "Parfois c'est effectivement une transition plus importante. "
            "Un coaching professionnel peut aider à y voir plus clair."
        ),
        "display_order": 3,
    },

    # ══════════════════════════════════════════════════════
    # FAMILLE 10 — Équilibre de vie & sécurité
    # ══════════════════════════════════════════════════════
    {
        "theme_code":       "equilibre_securite",
        "title":            "Équilibre de vie : trouver son rythme durable",
        "ultra_short_text": "Construire un équilibre qui tient",
        "short_text": (
            "L'équilibre vie pro / vie perso n'est pas un état stable à atteindre une fois "
            "pour toutes. C'est une dynamique à ajuster en permanence, selon les périodes et "
            "les priorités de vie."
        ),
        "long_text": (
            "## L'équilibre n'est pas une partition 50/50\n\n"
            "L'idée d'un équilibre parfait — autant de temps et d'énergie pour le pro "
            "et le perso — est souvent irréaliste. Les périodes de vie varient : "
            "certains moments demandent plus d'investissement professionnel, d'autres "
            "davantage de présence personnelle. Ce qui compte, c'est que ces déséquilibres "
            "soient temporaires et choisis — pas subis.\n\n"
            "## Les frontières comme outil\n\n"
            "Les frontières entre vie pro et vie perso se négocient — avec son employeur, "
            "mais aussi avec soi-même. Des rituels de transition (une marche après le travail, "
            "un changement de tenue, une activité physique) aident le cerveau à 'changer de mode'.\n\n"
            "**Définir ses non-négociables** : quelles sont les activités, relations ou rituels "
            "personnels auxquels on ne renonce pas, quelle que soit la pression professionnelle ?\n\n"
            "## Les signaux d'alerte\n\n"
            "Quand la vie personnelle s'efface complètement (pas de loisirs, relations négligées, "
            "santé ignorée), ce n'est pas un signe de performance — c'est un signe de vulnérabilité. "
            "Les personnes les plus performantes sur le long terme maintiennent des ressources "
            "extérieures au travail."
        ),
        "display_order": 1,
    },
    {
        "theme_code":       "equilibre_securite",
        "title":            "Insécurité professionnelle : vivre avec l'incertitude",
        "ultra_short_text": "Apprivoiser l'insécurité professionnelle",
        "short_text": (
            "La peur de perdre son emploi ou d'être déplacé contre sa volonté "
            "est un facteur de stress chronique majeur. On ne peut pas toujours contrôler "
            "la situation — mais on peut renforcer sa position et sa résilience."
        ),
        "long_text": (
            "## L'insécurité professionnelle : une réalité contemporaine\n\n"
            "Les restructurations, transformations numériques et incertitudes économiques "
            "ont rendu l'insécurité professionnelle plus répandue. Elle touche des personnes "
            "compétentes et engagées, dans tous les secteurs. Ce n'est pas un jugement sur "
            "sa valeur — c'est un contexte.\n\n"
            "## Ce que l'insécurité fait psychologiquement\n\n"
            "L'incertitude sur l'avenir professionnel active les mêmes circuits cérébraux "
            "que la menace physique. Elle capte l'attention, réduit la capacité à se projeter "
            "et peut conduire à une paralysie ou à une hyperactivité non productive.\n\n"
            "## Ce qu'on peut faire\n\n"
            "**Distinguer le probable du possible** : qu'est-ce qui est réellement menacé, "
            "et qu'est-ce qui est une projection anxieuse ?\n\n"
            "**Renforcer son employabilité** : compétences, réseau, visibilité professionnelle. "
            "Ce travail de fond réduit la vulnérabilité, quelle que soit la situation.\n\n"
            "**Préparer des scénarios** : avoir réfléchi à ce qu'on ferait 'si' réduit "
            "la charge anxieuse. La préparation n'attire pas la catastrophe — elle la rend "
            "moins effrayante.\n\n"
            "**Chercher du soutien** : conjoint, ami, coach ou conseiller en évolution "
            "professionnelle. On ne navigue pas bien seul dans l'incertitude."
        ),
        "display_order": 2,
    },
    {
        "theme_code":       "equilibre_securite",
        "title":            "Options & ressources publiques : savoir où s'orienter",
        "ultra_short_text": "Les ressources disponibles pour vous aider",
        "short_text": (
            "Face à une situation professionnelle difficile, il existe des ressources "
            "et des interlocuteurs dont beaucoup ignorent l'existence ou la disponibilité."
        ),
        "long_text": (
            "## Les interlocuteurs disponibles en entreprise\n\n"
            "**Le médecin du travail** : souvent sous-estimé, il peut intervenir sur "
            "l'aménagement du poste, accompagner un retour après un arrêt, orienter "
            "vers des soins spécialisés. Il est soumis au secret médical.\n\n"
            "**L'assistant(e) social(e) du travail** : présent dans de nombreuses entreprises, "
            "il/elle accompagne les situations difficiles (santé, logement, difficultés "
            "financières, situations familiales).\n\n"
            "**Le CSE / CSSCT** : peut être sollicité pour des situations de risques "
            "psychosociaux ou de conditions de travail dégradées.\n\n"
            "## Les ressources externes\n\n"
            "**L'ANACT** (Agence Nationale pour l'Amélioration des Conditions de Travail) : "
            "ressources en ligne sur les risques psychosociaux, la qualité de vie au travail.\n\n"
            "**Le CPF** (Compte Personnel de Formation) : financement de formation, bilan "
            "de compétences, accompagnement à la transition professionnelle.\n\n"
            "**France Travail** : accompagnement à la mobilité professionnelle, droits "
            "en cas de rupture de contrat.\n\n"
            "**Les lignes d'écoute** : certaines mutuelles et prévoyances proposent des "
            "lignes d'écoute psychologique accessibles 24h/24."
        ),
        "display_order": 3,
    },
]

# Stats
NB_CONTENUS = len(CONTENUS)
THEMES      = list({c["theme_code"] for c in CONTENUS})
