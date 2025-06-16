# Utilise une image Python légère
FROM python:3.12-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie les dépendances en premier (pour optimiser le cache Docker)
COPY requirements.txt .

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie le code de l'application
COPY app/ ./app/

# Copie le fichier d'environnement (optionnel, car docker-compose gère aussi l'env_file)
COPY .env .env

# Expose le port (pour la documentation)
EXPOSE 8000

# Commande de lancement de l'API FastAPI avec hot reload désactivé pour la prod
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
