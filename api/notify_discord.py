import os
import requests
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()
WEBHOOK_URL = os.getenv("WEBHOOK_URL")


def notify_discord(message: str, status: str = "Succès"):
    """
    Envoie une notification formatée (embed) à Discord via Webhook.
    """
    if not WEBHOOK_URL:
        logger.warning("Aucune URL de webhook Discord n'est définie.")
        return

    embed = {
        "embeds": [
            {
                "title": "Résultats du pipeline",
                "description": message,
                "color": 5814783,
                "fields": [
                    {"name": "Status", "value": status, "inline": True}
                ],
            }
        ]
    }

    try:
        response = requests.post(WEBHOOK_URL, json=embed)
        if response.status_code != 204:
            logger.error(
                f"Erreur Discord : {response.status_code} - {response.text}"
            )
        else:
            logger.success("Notification Discord envoyée avec succès.")
    except Exception as e:
        logger.exception(f"Exception lors de l'envoi à Discord : {e}")
