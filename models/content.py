# ============================================================
# models/content.py — Table "contents" (catalogue éditorial santé)
# ============================================================

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base


class Content(Base):
    """
    Table : contents
    Catalogue des contenus santé proposés aux utilisateurs.
    Chaque contenu est associé à un thème (= une famille fonctionnelle).

    Exemple :
      theme_code="stress",
      title="Stress — l'essentiel (1 minute)",
      short_text="3 techniques rapides pour souffler...",
      long_text="Article complet sur la gestion du stress..."
    """

    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)

    # Code du thème auquel ce contenu est rattaché
    # Ex: "stress", "fatigue", "charge_mentale"...
    # Permet de filtrer les contenus par thème (GET /api/contents?theme=stress)
    theme_code = Column(String(100), nullable=False, index=True)

    # Titre affiché à l'utilisateur
    title = Column(String(300), nullable=False)

    # Version ultra-courte : accroche de quelques mots
    # Affichée dans les cartes de recommandation
    ultra_short_text = Column(String(500), nullable=True)

    # Version courte : résumé en 2-3 phrases
    # Affichée dans la zone de restitution
    short_text = Column(Text, nullable=True)

    # Version longue : l'article complet
    # Affiché quand l'utilisateur clique sur "Lire plus"
    long_text = Column(Text, nullable=True)

    # Statut du contenu : seuls les contenus "published" sont visibles
    # Valeurs possibles : "draft" (brouillon) ou "published" (publié)
    status = Column(String(20), default="draft", nullable=False)

    # Ordre d'affichage (pour trier les contenus d'un même thème)
    display_order = Column(Integer, default=0)

    # Horodatages
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Content id={self.id} theme={self.theme_code} title='{self.title[:30]}...'>"
