from fastapi import FastAPI
from app.notify_discord import notify_discord

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    notify_discord("🚀 L'API FastAPI vient de démarrer !", status="Démarrage")

@app.get("/health")
async def health():
    return {"status": "ok"}
