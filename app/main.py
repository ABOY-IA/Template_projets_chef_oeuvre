import os
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from contextlib import asynccontextmanager
from app.notify_discord import notify_discord
import mlflow

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

@asynccontextmanager
async def lifespan(app):
    notify_discord("🚀 L'API FastAPI vient de démarrer !", status="Démarrage")
    yield

app = FastAPI(
    title="API IA Projets Chef d'Œuvre",
    description="API FastAPI pour l'orchestration IA, notifications et monitoring",
    version="1.0.0",
    lifespan=lifespan
)

# Modèles Pydantic pour les entrées/sorties
class PredictRequest(BaseModel):
    data: List[float]

class PredictResponse(BaseModel):
    prediction: float

class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    result: str

# Endpoint de healthcheck
@app.get("/health", tags=["Monitoring"])
async def health():
    return {"status": "ok"}

# Endpoint de prédiction avec tracking MLflow
@app.post("/predict", response_model=PredictResponse, tags=["IA"])
async def predict(request: PredictRequest):
    try:
        if not request.data:
            raise ValueError("La liste de données ne peut pas être vide.")
        prediction = sum(request.data) / len(request.data)
        # Tracking MLflow
        with mlflow.start_run(run_name="predict"):
            mlflow.log_param("nb_inputs", len(request.data))
            mlflow.log_metric("prediction", prediction)
        return PredictResponse(prediction=prediction)
    except Exception as e:
        notify_discord(f"Erreur /predict : {str(e)}", status="Erreur")
        raise HTTPException(status_code=400, detail=f"Erreur lors de la prédiction : {str(e)}")

# Endpoint de génération (exemple fictif)
@app.post("/generate", response_model=GenerateResponse, tags=["IA"])
async def generate(request: GenerateRequest):
    try:
        result = f"Résultat généré pour le prompt : {request.prompt}"
        return GenerateResponse(result=result)
    except Exception as e:
        notify_discord(f"Erreur /generate : {str(e)}", status="Erreur")
        raise HTTPException(status_code=400, detail=f"Erreur lors de la génération : {str(e)}")

# Endpoint de retrain avec tracking MLflow
@app.post("/retrain", tags=["IA"])
async def retrain():
    try:
        notify_discord("Déclenchement du retrain via l’API", status="Info")
        # Tracking MLflow pour retrain (simulation)
        with mlflow.start_run(run_name="retrain"):
            mlflow.log_param("event", "retrain_triggered")
            mlflow.log_metric("status", 1)
        return {"message": "Retrain déclenché (simulation)"}
    except Exception as e:
        notify_discord(f"Erreur /retrain : {str(e)}", status="Erreur")
        raise HTTPException(status_code=500, detail=f"Erreur lors du retrain : {str(e)}")

# Gestion globale des erreurs inattendues
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    notify_discord(f"Erreur inattendue : {str(exc)}", status="Erreur")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erreur interne du serveur"}
    )
