import requests
import json
import time
from datetime import datetime

NOTION_TOKEN = "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"
NOTION_DATABASE_ID = "222e43cf42f5809e969a000cebc28997"


def get_annonces():
    url = "https://api.leboncoin.fr/finder/search"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Leboncoin/5.5.0 (iPhone; iOS 15.1; Scale/3.00)"
    }

    payload = {
        "limit": 10,
        "offset": 0,
        "filters": {
            "category": {"id": "10"},
            "enums": {
                "real_estate_type": ["1"]
            }
        },
        "location": {
            "locations": [{
                "zipcode": "75000",
                "city": "Paris",
                "department_id": "75"
            }]
        },
        "sort_by": "time",
        "sort_order": "desc"
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    annonces = data.get("ads", [])
    print(f"Annonces trouvées : {len(annonces)}")
    for a in annonces:
        print(f"- {a['title']} ({a['price']} €) - {a['location'].get('city')}")

get_annonces()
