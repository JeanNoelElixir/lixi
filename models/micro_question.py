# ============================================================
# models/micro_question.py — Tables des micro-questions et réponses
# ============================================================
# Ce fichier contient DEUX modèles liés :
#   1. MicroQuestion : la bibliothèque de questions disponibles
#   2. MicroAnswer   : les réponses d'un utilisateur à une question

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class MicroQuestion(Base):
    """
    Table : micro_questions
    Catalogue de toutes les questions disponibles dans LIXIA.
    Ces questions sont sélectionnées dynamiquement selon l'humeur et le contexte.

    Exemple :
      code="Q7", text="Avez-vous pu vous déconnecter ce week-end ?",
      family="Fatigue & récupération", mood_trigger="TIRED"
    """

    __tablename__ = "micro_questions"

    id = Column(Integer, primary_key=True, index=True)

    # Code unique de la question (ex: "Q7", "Q12"...)
    # Utilisé dans les réponses pour savoir à quelle question ça correspond
    code = Column(String(20), nullable=False, unique=True, index=True)

    # Texte de la question affichée à l'utilisateur
    text = Column(Text, nullable=False)

    # Famille fonctionnelle concernée (ex: "Fatigue & récupération")
    # Correspond aux 10 familles de la spec
    family_code = Column(String(100), nullable=False)

    # Humeur(s) qui déclenchent cette question (ex: "TIRED", "ANXIOUS")
    # On stocke comme texte simple pour le MVP (ex: "TIRED,ANXIOUS")
    mood_trigger = Column(String(200), nullable=True)

    # Libellés des réponses stockés en JSON (ex: '["Pas du tout","Un peu",...]')
    # On utilise Text car SQLite ne supporte pas le type JSON natif
    reponses_json = Column(Text, nullable=True)

    # Scores correspondants aux réponses, stockés en JSON (ex: '[100,75,50,25,0]')
    scores_json = Column(Text, nullable=True)

    # La question est-elle active ? (permet de désactiver sans supprimer)
    is_active = Column(Boolean, default=True)

    # Relation vers les réponses
    answers = relationship("MicroAnswer", back_populates="question")

    def __repr__(self):
        return f"<MicroQuestion code={self.code} family={self.family_code}>"


class MicroAnswer(Base):
    """
    Table : micro_answers
    Stocke la réponse d'un utilisateur à une micro-question.
    Le score va de 0 (très négatif) à 100 (très positif).

    Exemple :
      user_id=42, question_code="Q7", score=25
      → L'utilisateur 42 a répondu 25/100 à la question Q7
    """

    __tablename__ = "micro_answers"

    id = Column(Integer, primary_key=True, index=True)

    # Lien vers l'utilisateur qui a répondu
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Code de la question à laquelle on répond
    # On fait référence au code (String) plutôt qu'à l'id pour plus de lisibilité
    question_code = Column(String(20), ForeignKey("micro_questions.code"), nullable=False)

    # Score de la réponse : 0 = très mauvais, 100 = très bon
    score = Column(Float, nullable=False)

    # Horodatage automatique
    inserted_at = Column(DateTime, server_default=func.now())

    # --- Relations ---
    user = relationship("User", back_populates="micro_answers")
    question = relationship("MicroQuestion", back_populates="answers")

    def __repr__(self):
        return f"<MicroAnswer user_id={self.user_id} question={self.question_code} score={self.score}>"
