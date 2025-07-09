import requests
import json
import time
from datetime import datetime

NOTION_TOKEN = "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"
NOTION_DATABASE_ID = "222e43cf42f5809e969a000cebc28997"

import requests

# Liste des villes que tu veux surveiller (sensible à la casse !)
#VILLES_CIBLEES = {"Laval", "Changé", "Saint-Berthevin", "Louverné", "L'Huisserie"}
# Liste des codes postaux que tu veux cibler
ZIPCODES_CIBLES = {"5300", "53810", "53950", "53940", "53970"}  # <-- adapte à tes besoins

# Paramètres de la requête API
url = "https://api.leboncoin.fr/finder/search"
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Leboncoin/5.5.0 (iPhone; iOS 15.1; Scale/3.00)"
}

payload = {
    "limit": 5000,
    "offset": 0,
    "filters": {
        "category": {"id": "9"},  # Ventes immobilières
        "enums": {
            "real_estate_type": ["1"],  # Maison
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
response = requests.post(url, headers=headers, json=payload)
data = response.json()

annonces = data.get("ads", [])
print(f"Annonces trouvées : {len(annonces)}")

for ad in annonces:
    titre = ad.get("subject", "Sans titre")
    prix = ad.get("price", ["?"])[0]
    lien = ad.get("url")    
    #ville = ad.get("location", {}).get("city")
    #if ville not in VILLES_CIBLEES:
    #    continue  # Ignore si la ville n'est pas ciblée
    print(f"** {titre} ([{prix}] €) - {ville} : {lien}")
    # Vérifie que le code postal de l'annonce est dans ta liste
    zipcode = ad.get("location", {}).get("zipcode")
    if zipcode not in ZIPCODES_CIBLES:
        continue  # Ignore cette annonce
    

    print(f"- {titre} ([{prix}] €) - {ville} : {lien}")

