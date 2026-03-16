# ============================================================
# routers/users.py — Routes API pour les utilisateurs
# ============================================================
# Un "router" FastAPI = un groupe de routes qui partagent
# le même préfixe et la même logique.
#
# Routes gérées ici :
#   GET  /api/user?user_id=...   → lire un profil
#   POST /api/user               → créer un profil

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db          # La fonction qui ouvre/ferme la session DB
from models.user import User         # Le modèle SQLAlchemy (= la table)
from schemas import UserCreate, UserOut  # Les schemas Pydantic (= les contrats)


# APIRouter() crée un mini-groupe de routes
# On lui donnera un préfixe "/api" dans main.py
router = APIRouter()


@router.get("/user", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Récupère le profil d'un utilisateur par son ID.

    - user_id : passé dans l'URL → GET /api/user?user_id=42
    - db      : session base de données injectée automatiquement par FastAPI
                grâce à Depends(get_db) — on n'a pas à l'appeler manuellement

    Retourne le profil ou une erreur 404 si l'utilisateur n'existe pas.
    """

    # db.query(User) = "je veux chercher dans la table users"
    # .filter(...)   = "où l'id correspond"
    # .first()       = "donne-moi le premier résultat (ou None si vide)"
    user = db.query(User).filter(User.id == user_id).first()

    # Si aucun utilisateur trouvé → erreur HTTP 404
    # HTTPException interrompt la requête et renvoie un message d'erreur au front
    if not user:
        raise HTTPException(status_code=404, detail=f"Utilisateur {user_id} introuvable")

    # FastAPI utilise UserOut pour formater la réponse automatiquement
    return user


@router.get("/user/by-email", response_model=UserOut)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """
    Retrouve un utilisateur par son adresse email.
    Utilisé par le front pour la reconnexion sans mot de passe.

    - email : passé dans l'URL → GET /api/user/by-email?email=marie@example.com
    - Retourne 404 si aucun compte trouvé avec cet email
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Aucun compte trouvé pour cet email")
    return user


@router.post("/user", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Crée un nouveau profil utilisateur.

    - payload : le corps JSON de la requête, validé automatiquement par UserCreate
    - status_code=201 : "201 Created" (convention REST pour une création réussie)
    """

    # Vérifier qu'un utilisateur avec cet email n'existe pas déjà
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        # 409 Conflict : la ressource existe déjà
        raise HTTPException(status_code=409, detail="Un compte existe déjà avec cet email")

    # Créer l'objet User à partir des données validées
    # payload.model_dump() = convertit le schema Pydantic en dictionnaire Python
    # Ex: {"first_name": "Jean", "email": "jean@lixi.fr", ...}
    new_user = User(**payload.model_dump())

    # Ajouter l'objet à la session (pas encore en base !)
    db.add(new_user)

    # Valider et écrire en base de données
    db.commit()

    # Recharger l'objet depuis la base pour avoir l'id et les valeurs auto-générées
    db.refresh(new_user)

    return new_user
