import os
import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def notify_discord(message: str, status: str = "Succès"):
    """
    Envoie une notification formatée (embed) à Discord via Webhook.
    """
    if not WEBHOOK_URL:
        print("Aucune URL de webhook Discord n'est définie.")
        return

    embed = {
        "embeds": [{
            "title": "Résultats du pipeline",
            "description": message,
            "color": 5814783,  # Couleur bleue (hex: 0x58B9FF)
            "fields": [
                {
                    "name": "Status",
                    "value": status,
                    "inline": True
                }
            ]
        }]
    }
    response = requests.post(WEBHOOK_URL, json=embed)
    if response.status_code != 204:
        print(f"Erreur Discord : {response.status_code} - {response.text}")
    else:
        print("Notification Discord envoyée avec succès.")
