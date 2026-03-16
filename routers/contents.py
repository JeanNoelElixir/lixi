# ============================================================
# routers/contents.py — Routes API pour les contenus santé
# ============================================================
# Routes gérées ici :
#   GET /api/contents?theme=stress  → liste par thème
#   GET /api/contents/:id           → un contenu complet

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models.content import Content
from schemas import ContentOut

router = APIRouter()


@router.get("/contents", response_model=List[ContentOut])
def get_contents(theme: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Retourne la liste des contenus santé publiés.

    - theme : filtre optionnel par thème (ex: ?theme=stress)
              Si absent → renvoie tous les contenus publiés

    Exemple :
      GET /api/contents           → tous les contenus
      GET /api/contents?theme=stress → contenus sur le stress uniquement
    """

    # On part de la requête de base : uniquement les contenus publiés
    query = db.query(Content).filter(Content.status == "published")

    # Si un thème est fourni, on filtre dessus
    if theme:
        query = query.filter(Content.theme_code == theme)

    # Trier par ordre d'affichage défini dans la base
    contents = query.order_by(Content.display_order).all()

    return contents


@router.get("/contents/{content_id}", response_model=ContentOut)
def get_content(content_id: int, db: Session = Depends(get_db)):
    """
    Retourne un contenu complet (y compris le long_text).

    - content_id : identifiant numérique dans l'URL → /api/contents/7
                   Les accolades {} dans le décorateur signalent un paramètre dynamique

    Exemple :
      GET /api/contents/7 → retourne l'article complet id=7
    """

    content = db.query(Content).filter(
        Content.id == content_id,
        Content.status == "published"   # On ne sert que les contenus publiés
    ).first()

    if not content:
        raise HTTPException(status_code=404, detail=f"Contenu {content_id} introuvable")

    return content
