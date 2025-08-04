import json
import requests
import os

API_URL_ORDERS = "http://localhost:5080/orders"

script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, "db-orders-history.json")
with open(json_path, "r", encoding="utf-8") as f:
    orders = json.load(f)

for order in orders:
    order.pop('mock', None)
    response = requests.post(API_URL_ORDERS, json=order)
    print(f"Ajout de {order.get('name', order.get('id', 'order'))}: {response.status_code} - {response.text}")