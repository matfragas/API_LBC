import requests
import json
import time
from datetime import datetime

NOTION_TOKEN = "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"
NOTION_DATABASE_ID = "222e43cf42f5809e969a000cebc28997"

import requests

# Liste des villes que tu veux surveiller (sensible à la casse !)
VILLES_CIBLEES = {"Laval", "Changé", "Saint-Berthevin", "Louverné", "L'Huisserie"}

# Paramètres de la requête API
url = "https://api.leboncoin.fr/finder/search"
payload = {
    "limit": 50,
    "offset": 0,
    "filters": {
        "category": {"id": "9"},  # Ventes immobilières
        "enums": {
            "real_estate_type": ["1", "2"],  # Maison et appartement
        },
        #"keywords": {
        #    "text": "",  # Pas de mot-clé particulier
        #    "type": "all"
        #},
        "location": {
            "department_id": "53", 
        }
    },
    "sort_by": "time"  # Trier par plus récent
}

# Appel à l'API
response = requests.post(url, json=payload)
data = response.json()

annonces = data.get("ads", [])
print(f"Annonces trouvées : {len(annonces)}")

for ad in annonces:
    ville = ad.get("location", {}).get("city")
    if ville not in VILLES_CIBLEES:
        continue  # Ignore si la ville n'est pas ciblée

    titre = ad.get("subject", "Sans titre")
    prix = ad.get("price", ["?"])[0]
    lien = ad.get("url")
    print(f"- {titre} ([{prix}] €) - {ville} : {lien}")

