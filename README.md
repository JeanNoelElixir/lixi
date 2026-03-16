# LIXI — Plateforme de bien-être au travail

## Démarrage local

```powershell
# Installer les dépendances
C:\Users\jnguignard\Python312\python.exe -m pip install -r requirements.txt

# Configurer l'environnement
Copy-Item .env.example .env
# Éditer .env et ajouter ANTHROPIC_API_KEY

# Lancer le back
C:\Users\jnguignard\Python312\python.exe -m uvicorn main:app --reload
```

Ouvrir `demo/index.html` dans le navigateur.

## Déploiement Render

1. Pousser le code sur GitHub
2. Créer un compte sur [render.com](https://render.com)
3. New → Blueprint → connecter le repo GitHub
4. Render lit `render.yaml` et crée automatiquement le service + la base PostgreSQL
5. Ajouter `ANTHROPIC_API_KEY` dans les variables d'environnement Render
6. Récupérer l'URL de déploiement (ex: `https://lixi-backend.onrender.com`)
7. Mettre à jour `demo/index-prod.html` avec cette URL
8. Activer GitHub Pages sur le repo → pointer vers `demo/index-prod.html`

## Variables d'environnement requises

| Variable | Description |
|---|---|
| `DATABASE_URL` | Fourni automatiquement par Render PostgreSQL |
| `ANTHROPIC_API_KEY` | Clé API Anthropic (console.anthropic.com) |
| `SECRET_KEY` | Généré automatiquement par Render |
| `APP_ENV` | `production` sur Render |
