import json
import requests
import os
import base64

API_URL = "http://localhost:5080/items"


script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "db-items-history.json")
with open(json_path, "r", encoding="utf-8") as f:
    items = json.load(f)

for item in items:
    # On retire la clé 'mock' si présente, car l'API ne la gère pas
    item.pop('mock', None)
    # Si le champ "photo" contient un lien, on convertit l'image en base64
    photo_url = item.get('photo')
    if photo_url and (photo_url.startswith('http://') or photo_url.startswith('https://')):
        try:
            img_response = requests.get(photo_url)
            if img_response.status_code == 200:
                img_type = img_response.headers.get('Content-Type', 'image/jpeg')
                base64_str = base64.b64encode(img_response.content).decode('utf-8')
                item['photo'] = f"data:{img_type};base64,{base64_str}"
            else:
                print(f"Impossible de télécharger l'image: {photo_url}")
        except Exception as e:
            print(f"Erreur lors de la récupération de l'image: {photo_url} - {e}")
    response = requests.post(API_URL, json=item)
    print(f"Ajout de {item.get('name')}: {response.status_code} - {response.text}")