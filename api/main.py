import os
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import List
from pydantic import BaseModel
import uvicorn

# Routers métier
from events import register_startup_events
from api.users.routes import router as users_router
from api.admin.routes import router as admin_router
from api.auth.routes import router as auth_router

# Services transversaux
from api.utils.logger import logger
from api.notify_discord import notify_discord
import mlflow
from prometheus_fastapi_instrumentator import Instrumentator

# --- Configuration MLflow ---
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


# --- Cycle de vie de l'application ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 L'API FastAPI démarre (startup event)")
    notify_discord("🚀 L'API FastAPI vient de démarrer !", status="Démarrage")
    yield


# --- Création de l'app FastAPI ---
app = FastAPI(
    title="FastAPI Template Projets Chef d'oeuvre (100% async)",
    description="API utilisateurs/sécurité, orchestration IA, monitoring, notifications.",
    version="1.0.0",
    lifespan=lifespan,
)

# --- Enregistrement d'événements supplémentaires ---
register_startup_events(app)

# --- Instrumentation Prometheus ---
Instrumentator().instrument(app).expose(app)

# --- Inclusion des routers principaux ---
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# --- Endpoints principaux ---


@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "Hello World"}


@app.get("/health", tags=["Monitoring"])
async def health() -> dict:
    logger.info("Appel endpoint /health")
    return {"status": "ok"}


# --- Modèles Pydantic pour l'IA ---
class PredictRequest(BaseModel):
    data: List[float]


class PredictResponse(BaseModel):
    prediction: float


class GenerateRequest(BaseModel):
    prompt: str


class GenerateResponse(BaseModel):
    result: str


# --- Endpoints IA ---


@app.post("/predict", response_model=PredictResponse, tags=["IA"])
async def predict(request: PredictRequest):
    logger.info(f"Appel endpoint /predict avec data={request.data}")
    try:
        if not request.data:
            raise ValueError("La liste de données ne peut pas être vide.")
        prediction = sum(request.data) / len(request.data)
        with mlflow.start_run(run_name="predict"):
            mlflow.log_param("nb_inputs", len(request.data))
            mlflow.log_metric("prediction", prediction)
        logger.success(f"Prédiction réussie: {prediction}")
        return PredictResponse(prediction=prediction)
    except Exception as e:
        logger.error(f"Erreur dans /predict : {e}")
        notify_discord(f"Erreur /predict : {str(e)}", status="Erreur")
        raise HTTPException(
            status_code=400, detail=f"Erreur lors de la prédiction : {str(e)}"
        )


@app.post("/generate", response_model=GenerateResponse, tags=["IA"])
async def generate(request: GenerateRequest):
    logger.info(f"Appel endpoint /generate avec prompt='{request.prompt}'")
    try:
        result = f"Résultat généré pour le prompt : {request.prompt}"
        logger.success("Génération réussie pour le prompt")
        return GenerateResponse(result=result)
    except Exception as e:
        logger.error(f"Erreur dans /generate : {e}")
        notify_discord(f"Erreur /generate : {str(e)}", status="Erreur")
        raise HTTPException(
            status_code=400, detail=f"Erreur lors de la génération : {str(e)}"
        )


@app.post("/retrain", tags=["IA"])
async def retrain():
    logger.info("Appel endpoint /retrain")
    try:
        notify_discord("Déclenchement du retrain via l’API", status="Info")
        with mlflow.start_run(run_name="retrain"):
            mlflow.log_param("event", "retrain_triggered")
            mlflow.log_metric("status", 1)
        logger.success("Retrain déclenché avec succès")
        return {"message": "Retrain déclenché (simulation)"}
    except Exception as e:
        logger.error(f"Erreur dans /retrain : {e}")
        notify_discord(f"Erreur /retrain : {str(e)}", status="Erreur")
        raise HTTPException(
            status_code=500, detail=f"Erreur lors du retrain : {str(e)}"
        )


# --- Gestion globale des exceptions ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Erreur inattendue sur {request.url.path}: {exc}")
    notify_discord(f"Erreur inattendue : {str(exc)}", status="Erreur")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erreur interne du serveur"},
    )


# --- Point d'entrée pour lancement local ---
if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
