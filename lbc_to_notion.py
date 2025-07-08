import requests
import json
import time
from datetime import datetime

NOTION_TOKEN = "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"
NOTION_DATABASE_ID = "222e43cf42f5809e969a000cebc28997"

def get_annonces(le_filter, limit=35, limit_pages=3):
    url = "https://api.leboncoin.fr/finder/search"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Leboncoin/5.5.0 (iPhone; iOS 15.1; Scale/3.00)"
    }

    all_ads = []
    offset = 0
    for _ in range(limit_pages):
        payload = {
            "filters": le_filter,
            "limit": limit,
            "offset": offset,
            "sort_by": "time",
            "sort_order": "desc"
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            ads = data.get("ads", [])
            if not ads:
                break
            all_ads.extend(ads)
            offset += limit
        else:
            print("Erreur API:", response.status_code)
            break

    return all_ads

def notion_page_exists(ad_id):
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    payload = {
        "filter": {
            "property": "LBC ID",
            "rich_text": {"equals": ad_id}
        }
    }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        data = res.json()
        return len(data.get("results", [])) > 0
    return False

def send_to_notion(ad):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    data = {
        "parent": { "database_id": NOTION_DATABASE_ID },
        "properties": {
            "Titre": {
                "title": [{"text": {"content": ad["title"]}}]
            },
            "Prix": {
                "number": ad.get("price", 0)
            },
            "Localisation": {
                "rich_text": [{"text": {"content": ad["location"].get("city", "")}}]
            },
            "URL": {
                "url": f"https://www.leboncoin.fr/vi/{ad['id']}.htm"
            },
            "LBC_ID": {
                "rich_text": [{"text": {"content": ad["id"]}}]
            }
        }
    }

    res = requests.post(url, headers=headers, json=data)
    if res.status_code != 200:
        print(f"Erreur envoi Notion: {res.status_code} {res.text}")

def main():
    filters = {
        "category": {"id": "10"},
        "real_estate_type": {"id": "1"},  # Vente
        "location": {
            "locations": [{"zipcode": "75000"}]
        }
    }

    annonces = get_annonces(filters, limit_pages=5)
    print(f"Annonces récupérées: {len(annonces)}")

    for ad in annonces:
        if not notion_page_exists(ad["id"]):
            send_to_notion(ad)
            print(f"Ajouté: {ad['title']}")
            time.sleep(0.5)
        else:
            print(f"Déjà présent: {ad['title']}")

if __name__ == "__main__":
    main()
