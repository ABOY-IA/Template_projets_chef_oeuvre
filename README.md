# Template pour Projets chef d'oeuvre

## Préparation du projet

### Lancement

1. Créer le fichier `.env` et renseigner les variables.
2. Construire et lancer les services :
`docker compose up --build -d`
3. Accéder à l’API : http://localhost:8000/health
4. Accéder à Uptime Kuma : http://localhost:3001

### Fonctionnalités

- Monitoring automatique de l’API
- Notification Discord à chaque démarrage de l’API

### Commandes Docker

Build complet et lancement de la stack :

`export COMPOSE_BAKE=true && docker compose up --build -d`

Nettoyer entièrement (images, volumes, orphelins) :
`docker compose down --rmi all --volumes --remove-orphans`

Relancer simplement (si déjà build) :

`docker compose up`

Arrêter la stack (tous les services) :

`docker compose down`

