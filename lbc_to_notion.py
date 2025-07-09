import requests
import time

CODES_POSTAUX_CIBLE = ["53000", "53810", "53940", "53950", "53970"]  # Alès, Nîmes, Uzès, etc.
MAX_OFFSETS = 100  # LeBonCoin limite à 100 résultats par recherche

def chercher_annonces_par_code_postal(code_postal):
    print(f"\n🔎 Récupération des annonces pour le code postal {code_postal}...")
    toutes_annonces = []
    for offset in range(0, MAX_OFFSETS, 50):
        url = "https://api.leboncoin.fr/finder/search"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Leboncoin/5.5.0 (iPhone; iOS 15.1; Scale/3.00)"
        }
        payload = {
            "limit": 50,
            "offset": offset,
            "filters": {
                "category": {"id": "9"},  # Immobilier > Vente
                "enums": {
                    "real_estate_type": ["1", "2"]  # Maison, Appartement
                },
                "keywords": {
                    "text": "",
                    "type": "all"
                },
                "location": {
                    "zipcodes": [code_postal]
                }
            },
            "sort_by": "time"
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"❌ Erreur pour {code_postal} : {response.status_code}")
            break

        data = response.json()
        annonces = data.get("ads", [])

        if not annonces:
            break

        toutes_annonces.extend(annonces)
        time.sleep(0.5)  # Pause anti-blocage

    print(f"✅ {len(toutes_annonces)} annonces récupérées pour {code_postal}")
    return toutes_annonces


# Récupérer toutes les annonces pour chaque code postal
annonces_filtrees = []
for code in CODES_POSTAUX_CIBLE:
    annonces_cp = chercher_annonces_par_code_postal(code)
    annonces_filtrees.extend(annonces_cp)
    print(f"\n ** Code : {code}")
    print(f"\n ** annonces_cp : {annonces_cp}")
    print(f"\n ** annonces_filtrees.extend(annonces_cp) : {annonces_filtrees.extend(annonces_cp)}")

print(f"\n🎉 Total annonces récupérées : {len(annonces_filtrees)}")

# Exemple : afficher les annonces résumées
for ad in annonces_filtrees:
    print(f"- {ad.get('subject')} ({ad.get('price', ['?'])[0]} €) - {ad.get('location', {}).get('city')} - {ad.get('url')}")
