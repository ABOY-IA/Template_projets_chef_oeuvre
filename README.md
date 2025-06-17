# Template pour Projets chef d'oeuvre

## Préparation du projet

### Lancement

1. Créer le fichier `.env` et renseigner les variables en se basant sur ce modèle :
```
# FastAPI
API_PORT=8000

# Prefect
PREFECT_API_URL=http://prefect-server:4200/api
PREFECT_WORK_POOL=default-work-pool

# PostgreSQL (pour Prefect)
POSTGRES_USER=xxxx
POSTGRES_PASSWORD=xxxx
POSTGRES_DB=xxxx
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Prefect DB connection string
PREFECT_API_DATABASE_CONNECTION_URL=postgresql+asyncpg://prefect:prefect@postgres:5432/prefect

# Discord Webhook (ne jamais exposer en clair dans le code)
WEBHOOK_URL=https://discord.com/api/webhooks/
```

2. Construire et lancer les services.
3. Accéder à l’API : http://localhost:8000/health
4. Accéder à Uptime Kuma : http://localhost:3001

### Fonctionnalités

- Monitoring automatique de l’API
- Notification Discord à chaque démarrage de l’API
- Commande pour créer la work-pool :
     Se déplacer dans le dossier qui contient son fichier de flow puis exécuter :
        `prefect work-pool create --type process default-work-pool`
- Commande pour créer le fichier yaml qui permet le deployment dans Prefect UI :
    - Se déplacer dans le dossier qui contient son fichier de flow puis exécuter :
        `prefect deployment build flow.py:periodic_check -n random-check --pool default-work-pool --work-queue default`
        `prefect deployment apply periodic_check-deployment.yaml`

### Commandes Docker

Build complet et lancement de la stack :

`export COMPOSE_BAKE=true && docker compose up --build -d`

Nettoyer entièrement (images, volumes, orphelins) :
`docker compose down --rmi all --volumes --remove-orphans`
Adapter pour ne supprimer que les images ou tout sauf les volumes pour ne pas recréer le compte admin Uptime Kuma.

Reconstruire les services si modifications dans code ou requirements ou Dockerfile :

`docker compose build --no-cache`

Relancer simplement (si déjà build) :

`docker compose up -d`

Arrêter la stack (tous les services) :

`docker compose down`

