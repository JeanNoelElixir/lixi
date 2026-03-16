# ============================================================
# models/questionnaire.py — Tables des questionnaires COPSOQ / WHOCOL
# ============================================================
# Ce fichier contient DEUX modèles :
#   1. QuestionnaireItem    : le catalogue de toutes les questions
#   2. QuestionnaireAnswer  : les réponses d'un utilisateur

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class QuestionnaireItem(Base):
    """
    Table : questionnaire_items
    Catalogue de toutes les questions COPSOQ et WHOCOL.
    Chargé une seule fois au démarrage depuis les données de l'Excel.

    Chaque ligne = une question avec ses 4 ou 5 modalités de réponse
    et le score correspondant à chaque modalité.
    """

    __tablename__ = "questionnaire_items"

    id = Column(Integer, primary_key=True, index=True)

    # Source : "copsoq" ou "whocol"
    source = Column(String(20), nullable=False, index=True)

    # Code unique de la question (ex: "copsoq7", "8 (F16.1)")
    code = Column(String(50), nullable=False, unique=True, index=True)

    # Domaine thématique (ex: "Domaine des contraintes quantitatives")
    domaine = Column(String(200), nullable=True)

    # Catégorie dans le domaine (ex: "Charge de travail")
    categorie = Column(String(200), nullable=True)

    # Texte complet de la question posée à l'utilisateur
    item = Column(Text, nullable=False)

    # Libellés des modalités de réponse (stockés en JSON)
    # Ex: ["Toujours", "Souvent", "Parfois", "Rarement", "Jamais"]
    reponses = Column(JSON, nullable=False)

    # Scores associés à chaque réponse (stockés en JSON)
    # Ex: [0, 25, 50, 75, 100]
    # L'index correspond à la réponse choisie : reponses[2] → scores[2]
    scores = Column(JSON, nullable=False)

    # La question est-elle active dans le questionnaire courant ?
    is_active = Column(Boolean, default=True)

    # Relation vers les réponses données par les utilisateurs
    answers = relationship("QuestionnaireAnswer", back_populates="item")

    def score_pour_reponse(self, index_reponse: int) -> float:
        """
        Retourne le score correspondant à une réponse choisie.

        Exemple : si l'utilisateur choisit la 3ème option (index=2)
        et que scores = [0, 25, 50, 75, 100] → retourne 50.0
        """
        if index_reponse < 0 or index_reponse >= len(self.scores):
            raise ValueError(f"Index de réponse invalide : {index_reponse}")
        score = self.scores[index_reponse]
        # Certaines questions ont None pour la 5ème réponse (ex: copsoq38 à 4 modalités)
        if score is None:
            raise ValueError(f"Réponse {index_reponse} non disponible pour {self.code}")
        return float(score)

    def __repr__(self):
        return f"<QuestionnaireItem source={self.source} code={self.code}>"


class QuestionnaireAnswer(Base):
    """
    Table : questionnaire_answers
    Stocke les réponses d'un utilisateur aux questionnaires COPSOQ / WHOCOL.

    Un utilisateur peut répondre plusieurs fois dans le temps.
    On garde l'historique complet pour les calculs de tendance.
    """

    __tablename__ = "questionnaire_answers"

    id = Column(Integer, primary_key=True, index=True)

    # Lien vers l'utilisateur
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                     nullable=False, index=True)

    # Source du questionnaire : "copsoq" ou "whocol"
    source = Column(String(20), nullable=False)

    # Code de la question (référence vers questionnaire_items.code)
    question_code = Column(String(50), ForeignKey("questionnaire_items.code"),
                           nullable=False)

    # Score calculé (0-100), pas l'index de la réponse — déjà converti
    # C'est ce score qui sera utilisé par le moteur LIXIA
    score = Column(Float, nullable=False)

    # Index de la réponse choisie (0-4) — pour affichage et audit
    reponse_index = Column(Integer, nullable=True)

    # Date d'enregistrement
    inserted_at = Column(DateTime, server_default=func.now())

    # --- Relations ---
    user = relationship("User", back_populates="questionnaire_answers")
    item = relationship("QuestionnaireItem", back_populates="answers")

    def __repr__(self):
        return (f"<QuestionnaireAnswer user_id={self.user_id} "
                f"source={self.source} code={self.question_code} score={self.score}>")
