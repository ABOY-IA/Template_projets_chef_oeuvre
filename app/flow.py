import os
import random
from prefect import flow, task, get_run_logger
from dotenv import load_dotenv

from notify_discord import notify_discord

# Charge toutes les variables d'environnement depuis le .env
load_dotenv()

PREFECT_API_URL = os.getenv("PREFECT_API_URL")
PREFECT_FLOW_INTERVAL = int(os.getenv("PREFECT_FLOW_INTERVAL", 10))

@task(retries=2, retry_delay_seconds=1)
def check_random():
    logger = get_run_logger()
    value = random.random()
    logger.info(f"Nombre aléatoire généré : {value:.3f}")

    if value < 0.5:
        logger.warning("Valeur < 0.5, déclenchement du retrain.")
        notify_discord("Valeur < 0.5 détectée dans le pipeline Prefect. Déclenchement du retrain.", status="Alerte")
        # Place ici l'appel à ta fonction de retrain si besoin
    else:
        logger.info("Valeur >= 0.5, pas d'action.")
        notify_discord("Pipeline Prefect : tout est ok (valeur >= 0.5).", status="OK")

@flow(name="random-check")
def periodic_check():
    check_random()
