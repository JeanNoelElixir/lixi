# ============================================================
# models/__init__.py — Point d'entrée des modèles
# ============================================================
from models.user           import User
from models.mood           import Mood
from models.micro_question import MicroQuestion, MicroAnswer
from models.content        import Content
from models.coach_request  import CoachRequest
from models.questionnaire  import QuestionnaireItem, QuestionnaireAnswer

from sqlalchemy.orm import relationship

# Relations retour sur User (évite les imports circulaires)
User.moods                   = relationship("Mood",                 back_populates="user", cascade="all, delete")
User.micro_answers           = relationship("MicroAnswer",          back_populates="user", cascade="all, delete")
User.coach_requests          = relationship("CoachRequest",         back_populates="user", cascade="all, delete")
User.questionnaire_answers   = relationship("QuestionnaireAnswer",  back_populates="user", cascade="all, delete")
