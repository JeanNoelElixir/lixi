# ============================================================
# models/coach_request.py — Table "coach_requests" (demandes coaching)
# ============================================================

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


# Niveaux d'urgence possibles pour une demande de coaching
URGENCY_LEVELS = {
    "low":    "Pas urgent — dans les prochaines semaines",
    "medium": "Assez urgent — cette semaine",
    "high":   "Urgent — dès que possible"
}


class CoachRequest(Base):
    """
    Table : coach_requests
    Enregistre les demandes de coaching envoyées par les utilisateurs.

    Un utilisateur peut demander un coaching quand sa priorité dépasse 75.
    Un cooldown (délai minimum entre deux demandes) est géré côté logique métier.
    """

    __tablename__ = "coach_requests"

    id = Column(Integer, primary_key=True, index=True)

    # Lien vers l'utilisateur qui fait la demande
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Sujet principal de la demande (ex: "Surcharge / pression", "Conflits au travail"...)
    topic = Column(String(300), nullable=False)

    # Niveau d'urgence : "low", "medium" ou "high"
    urgency = Column(String(20), nullable=False, default="medium")

    # Contexte libre rédigé par l'utilisateur
    # "Décrivez votre situation en quelques mots"
    context_text = Column(Text, nullable=True)

    # Objectif de l'utilisateur pour ce coaching
    # "Qu'espérez-vous retirer de cet échange ?"
    goal_text = Column(Text, nullable=True)

    # Statut de traitement de la demande
    # "pending" = en attente, "processed" = traitée, "cancelled" = annulée
    status = Column(String(20), default="pending", nullable=False)

    # Horodatage : date et heure de la demande
    inserted_at = Column(DateTime, server_default=func.now())

    # --- Relation ---
    user = relationship("User", back_populates="coach_requests")

    def __repr__(self):
        return f"<CoachRequest user_id={self.user_id} topic='{self.topic}' urgency={self.urgency}>"
