import requests
import time

VILLES_CIBLEES = ["Laval", "Changé", "L'huisserie", "Louverné", "Saint-Berthevin"]
MAX_OFFSETS = 100  # Car LeBonCoin ne donne que les annonces avec offset <= 100

def chercher_annonces_par_ville(ville):
    print(f"\n🔎 Récupération des annonces pour {ville}...")
    toutes_annonces = []
    for offset in range(0, MAX_OFFSETS, 50):
        payload = {
            "limit": 50,
            "offset": offset,
            "filters": {
                "category": {"id": "9"},  # Ventes immobilières
                "enums": {
                    "real_estate_type": ["1"],  # Maison
                },
                "keywords": {
                    "text": "",
                    "type": "all"
                },
                "location": {
                    "city": ville
                }
            },
            "sort_by": "time"
        }

        response = requests.post("https://api.leboncoin.fr/finder/search", json=payload)
        data = response.json()
        annonces = data.get("ads", [])

        if not annonces:
            break

        toutes_annonces.extend(annonces)
        time.sleep(0.5)  # éviter d'être bloqué

    print(f"✅ {len(toutes_annonces)} annonces récupérées pour {ville}")
    return toutes_annonces


# Récupérer toutes les annonces filtrées ville par ville
annonces_filtrees = []
for ville in VILLES_CIBLEES:
    annonces_ville = chercher_annonces_par_ville(ville)
    annonces_filtrees.extend(annonces_ville)

print(f"\n🎉 Total annonces récupérées : {len(annonces_filtrees)}")

# Exemple de traitement ou affichage
for ad in annonces_filtrees:
    print(f"- {ad.get('subject')} ({ad.get('price', ['?'])[0]} €) - {ad.get('location', {}).get('city')} - {ad.get('url')}")
