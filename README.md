# Template pour Projets chef d'oeuvre

## Préparation du projet

### Lancement

1. Créer le fichier `.env` et renseigner les variables en se basant sur ce modèle :
```
#######################
# --- API FastAPI --- #
#######################

API_PORT=8000
API_URL=http://api:8000

# Clé secrète pour JWT (à personnaliser en prod)
SECRET_KEY=changeme_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ADMIN_CREATION_SECRET=changeme_admin_secret

# Discord Webhook (dummy pour CI, à remplacer en prod)
WEBHOOK_URL=https://discord.com/api/webhooks/dummy/dummy

###########################
# --- Base de données --- #
###########################

# Pour le service db (postgres-custom)
DB_HOST=db
DB_PORT=5432
DB_WAIT_TIMEOUT=120
POSTGRES_USER=ci_admin
POSTGRES_PASSWORD=ci_admin_pass
POSTGRES_DB=ci_db

# Pour Prefect (utilisé par l'app, pas par Postgres à l'init)
PREFECT_DB_USER=ci_prefect_user
PREFECT_DB_PASSWORD=ci_prefect_pass
PREFECT_DB_NAME=ci_prefect_db

# URL SQLAlchemy pour Prefect server
PREFECT_API_DATABASE_CONNECTION_URL=postgresql+asyncpg://ci_prefect_user:ci_prefect_pass@db:5432/ci_prefect_db

# URL SQLAlchemy pour l'API principale
DATABASE_URL=postgresql://ci_admin:ci_admin_pass@db:5432/ci_db

##########################
# --- Prefect --- #
##########################

PREFECT_API_URL=http://prefect-server:4200/api
PREFECT_WORK_POOL=default-work-pool
PREFECT_SERVER_PORT=4200

##########################
# --- MLflow --- #
##########################

MLFLOW_PORT=5000
MLFLOW_ARTIFACT_ROOT=/mlflow/artifacts
MLFLOW_BACKEND_STORE_URI=sqlite:////mlflow_data/mlflow.db

##########################
# --- Monitoring --- #
##########################

PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
UPTIME_KUMA_PORT=3001

##########################
# --- Frontend --- #
##########################

FRONTEND_PORT=8501
STREAMLIT_BROWSER_GATHERUSAGESTATS=false

##########################
# --- Divers / Options --- #
##########################

# Compose bake (optionnel)
COMPOSE_BAKE=true
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

Build complet sans cache :

`export COMPOSE_BAKE=true && docker compose build --no-cache`

Lancement de la stack :

`export COMPOSE_BAKE=true && docker compose up -d`

Nettoyer entièrement (images, volumes, orphelins) :
`docker compose down --rmi all --volumes --remove-orphans`
Adapter pour ne supprimer que les images ou tout sauf les volumes pour ne pas recréer le compte admin Uptime Kuma.

Reconstruire les services si modifications dans code ou requirements ou Dockerfile :

`docker compose build --no-cache`

Relancer simplement (si déjà build) :

`docker compose up -d`

Arrêter la stack (tous les services) :

`docker compose down`

Nettoie tout le disque dur de tous les fichiers et service :

`docker system prune`

### Créer un compte admin

`docker-compose run --rm api python create_admin.py`

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

```
.
├── README.md
├── api
│   ├── Dockerfile
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── events.cpython-312.pyc
│   │   ├── logger.cpython-312.pyc
│   │   └── main.cpython-312.pyc
│   ├── admin
│   │   ├── __pycache__
│   │   │   └── routes.cpython-312.pyc
│   │   └── routes.py
│   ├── auth
│   │   ├── __pycache__
│   │   │   └── routes.cpython-312.pyc
│   │   └── routes.py
│   ├── core
│   │   ├── __pycache__
│   │   │   ├── crypto.cpython-312.pyc
│   │   │   ├── security.cpython-312.pyc
│   │   │   ├── testing_middleware.cpython-312.pyc
│   │   │   └── tokens.cpython-312.pyc
│   │   ├── crypto.py
│   │   ├── security.py
│   │   └── tokens.py
│   ├── create_admin.py
│   ├── db
│   │   ├── __pycache__
│   │   │   ├── base.cpython-312.pyc
│   │   │   ├── models.cpython-312.pyc
│   │   │   ├── schemas.cpython-312.pyc
│   │   │   ├── services.cpython-312.pyc
│   │   │   └── session.cpython-312.pyc
│   │   ├── base.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── services.py
│   │   └── session.py
│   ├── events.py
│   ├── flow.py
│   ├── main.py
│   ├── notify_discord.py
│   ├── periodic_check-deployment.yaml
│   ├── requirements.txt
│   ├── users
│   │   ├── __pycache__
│   │   │   └── routes.cpython-312.pyc
│   │   └── routes.py
│   ├── utils
│   │   └── logger.py
│   └── wait_for_db.py
├── docker-compose.yml
├── frontend
│   ├── Dockerfile
│   ├── app.py
│   ├── logs
│   ├── pages
│   │   ├── 0_login.py
│   │   ├── 1_profil.py
│   │   └── 2_administration.py
│   ├── requirements.txt
│   └── utils
│       ├── __pycache__
│       │   └── logger.cpython-312.pyc
│       └── logger.py
├── logs
│   └── frontend.log
├── models
├── monitoring
│   ├── grafana_data
│   ├── mlflow_data
│   │   └── mlflow.db
│   ├── mlruns
│   ├── prometheus_data
│   │   └── prometheus.yml
│   └── uptime-kuma-data
│       ├── docker-tls
│       ├── kuma.db
│       ├── screenshots
│       └── upload
├── pipelines
├── postgres-custom
│   ├── Dockerfile
│   ├── docker-entrypoint-init-custom.sh
│   ├── docker-entrypoint-initdb.d
│   │   └── init-users.sql
│   ├── pg_hba.conf
│   ├── postgresql.conf
│   ├── server.crt
│   └── server.key
├── pyproject.toml
├── pytest.ini
├── requirements.txt
└── tests
    ├── __pycache__
    │   ├── __init__.cpython-312.pyc
    │   ├── test_main.cpython-312-pytest-8.4.1.pyc
    │   └── test_minimal.cpython-312-pytest-8.4.1.pyc
    ├── conftest.py
    ├── test_admin.py
    ├── test_auth.py
    ├── test_co_db.py
    ├── test_main.py
    ├── test_monitoring.py
    ├── test_users.py
    ├── utils
    │   └── logger.py
    └── wait_for_api.py
```

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
