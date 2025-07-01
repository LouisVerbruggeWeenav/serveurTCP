
import requests
import time

for i in range(10):
    print(f"Envoi de la requête {i+1}...")

    response = requests.get("http://127.0.0.1:5000")
    print(response.text)
    time.sleep(4)

