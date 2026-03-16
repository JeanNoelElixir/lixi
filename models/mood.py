# ============================================================
# models/mood.py — Table "moods" (historique des humeurs)
# ============================================================

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship   # Pour lier deux tables entre elles
from sqlalchemy.sql import func
from database import Base


# Codes d'humeur valides selon la spec
# On les définit ici comme constantes pour les réutiliser facilement
MOOD_CODES = {
    "HAPPY":   "😊 Bien / Positif",
    "NEUTRAL": "😐 Neutre",
    "TIRED":   "😴 Fatigué(e)",
    "ANXIOUS": "😟 Anxieux/se",   # Correspond à "ANX" dans la spec
    "SAD":     "😢 Triste / Bas(se)"
}


class Mood(Base):
    """
    Table : moods
    Enregistre chaque check-in d'humeur d'un utilisateur.
    Un utilisateur peut avoir plusieurs humeurs (une par jour idéalement).
    """

    __tablename__ = "moods"

    # Identifiant unique de l'humeur
    id = Column(Integer, primary_key=True, index=True)

    # Clé étrangère : relie cette humeur à un utilisateur
    # ForeignKey("users.id") = "cette valeur doit exister dans la table users, colonne id"
    # ondelete="CASCADE" = si l'utilisateur est supprimé, ses humeurs le sont aussi
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Code de l'humeur choisie (ex: "HAPPY", "ANXIOUS"...)
    mood_code = Column(String(20), nullable=False)

    # Score numérique de l'humeur (0 = très négatif, 100 = très positif)
    # Ce score est calculé automatiquement depuis le mood_code
    score = Column(Float, nullable=False)

    # Commentaire libre optionnel saisi par l'utilisateur
    # Text() = texte long (pas de limite de taille fixe, contrairement à String)
    free_text = Column(Text, nullable=True)

    # Date/heure d'enregistrement (horodatage automatique)
    inserted_at = Column(DateTime, server_default=func.now())

    # --- Relation Python (pas une colonne, juste un lien logique) ---
    # Permet d'écrire mood.user pour accéder directement à l'objet User lié
    # back_populates="moods" = côté User, on pourra écrire user.moods
    user = relationship("User", back_populates="moods")

    def __repr__(self):
        return f"<Mood user_id={self.user_id} code={self.mood_code} score={self.score}>"
