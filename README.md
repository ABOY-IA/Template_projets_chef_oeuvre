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

# MLflow
MLFLOW_PORT=5000
MLFLOW_ARTIFACT_ROOT=/mlflow/artifacts
MLFLOW_BACKEND_STORE_URI=sqlite:////mlflow_data/mlflow.db

# Prometheus & Grafana
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
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

## 🐍 Environnement Python

### Prérequis

- Python 3.12 (recommandé)
- `pip` installé et mis à jour (inclus avec Python)
- Terminal ou shell (Linux, macOS, Windows PowerShell, Bash, etc.)

### Création et activation de l’environnement virtuel

À la racine du projet :

```
python3 -m venv .venv
```

Activation :
- Sous Linux / macOS :
    ```
    source .venv/bin/activate
    ```
- Sous Windows (PowerShell) :
    ```
    .venv\Scripts\Activate.ps1
    ```
- Sous Windows (CMD) :
    ```
    .venv\Scripts\activate.bat
    ```

Désactivation :
```
deactivate
```

Mettre à jour pip :
```
python -m pip install --upgrade pip
```

Installer les dépendances :
```
pip install -r requirements.txt
```

Générer ou mettre à jour le requirements.txt :
```
pip freeze > requirements.txt
```

---

## ⚙️ Configuration du fichier `.env`

Le fichier `.env` doit être créé à la racine du projet.  
Il contient toutes les variables d’environnement nécessaires au fonctionnement de l’application et à la configuration de Docker Compose.

**Exemple de contenu minimal :**
```
# Clé secrète utilisée pour signer et vérifier les JWT (doit être identique partout)
SECRET_KEY=supersecretkey123

# Algorithme utilisé pour les JWT (par défaut: HS256)
ALGORITHM=HS256

# Durée de vie des tokens access/refresh (en minutes/jours)
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Clé de création admin (si utilisée)
ADMIN_CREATION_SECRET=MonSecretSuperSecurise

# Connexion à la base Postgres
DATABASE_URL=postgresql://user:pass@db:5432/xtremdb

# Configuration de la base de données
DB_HOST=db
DB_PORT=5432
DB_WAIT_TIMEOUT=120
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=xtremdb

# URL de l'API (pour le frontend ou les tests)
API_URL=http://api:8000

# Désactive la télémétrie Streamlit
STREAMLIT_BROWSER_GATHERUSAGESTATS=false

# Compose bake (optionnel, selon ton usage)
COMPOSE_BAKE=true
```

---

## 🔒 Sécurité PostgreSQL

La base PostgreSQL est configurée pour :
- Authentification SCRAM-SHA-256
- Chiffrement SSL/TLS (certificats auto-signés par défaut)
- Connexions réseau sécurisées entre les services Docker

Les fichiers de configuration et certificats sont dans le dossier `postgres-custom/`, injectés automatiquement à l’initialisation.

---

## 🐳 Commandes Docker Compose

### Nettoyer entièrement (images, volumes, orphelins)
```
docker-compose down --rmi all --volumes --remove-orphans
```

### Build complet et lancement de la stack
```
export COMPOSE_BAKE=true
docker-compose up --build
```

### Relancer simplement (si déjà build)
```
docker-compose up
```

### Arrêter la stack (tous les services)
```
docker-compose down
```

### Lancer les tests unitaires
```
docker-compose run --rm tests
```

### Créer un compte admin
```
docker-compose run --rm api python create_admin.py
```

---

## 📁 Arborescence du projet



---

## 📝 Conseils et bonnes pratiques

- **Créer le `.env` avec les noms de variables indiqués dans l'exemple**
- **Vérifiez la cohérence des variables d’environnement entre le `.env` et le `docker-compose.yml`.**
- **Pour toute modification de la configuration PostgreSQL (SCRAM, SSL, etc.), nettoyez les volumes avant de rebuild.**
- **Pour ajouter des dépendances Python, modifiez le `requirements.txt` du dossier concerné puis rebuildez l’image correspondante.**
- **Consultez les logs dans le dossier `logs/` pour le debug.**

---

## 👨‍💻 Pour aller plus loin

- Ajoutez une CI/CD pour automatiser les tests et le déploiement.
- Ajoutez Prometheus/Grafana pour la supervision.
- Sécurisez les certificats SSL pour la production (utilisez une vraie CA).
- Ajoutez des scripts de migration si vous faites évoluer le schéma de la base.

---

# **By KaRn1zC**
