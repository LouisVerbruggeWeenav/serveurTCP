
import requests
import time

sendAccu = 0
while True:


    response = requests.get("http://51.254.102.27:5000")
    
    sendAccu += 1

    print(response.text)
    print(f"Envoi de la requête {sendAccu+1}...")
    time.sleep(2)

