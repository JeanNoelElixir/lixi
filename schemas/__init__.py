# ============================================================
# schemas/__init__.py — Point d'entrée des schemas
# ============================================================
# Même principe que models/__init__.py :
# on centralise tous les imports pour simplifier l'usage ailleurs.
#
# Dans les routers, on pourra écrire :
#   from schemas import UserCreate, UserOut, MoodCreate...
# au lieu d'importer chaque fichier séparément.

from schemas.user           import UserCreate, UserUpdate, UserOut
from schemas.mood           import MoodCreate, MoodOut
from schemas.micro_question import MicroQuestionOut, MicroAnswerCreate, MicroAnswerOut
from schemas.content        import ContentOut, ContentSummary
from schemas.coach_request  import CoachRequestCreate, CoachRequestOut
from schemas.analysis       import AnalysisOut, FamilyScore
from schemas.questionnaire import (
    QuestionnaireItemOut, QuestionnaireAnswerCreate,
    QuestionnaireAnswerOut, QuestionnaireSummary
)
