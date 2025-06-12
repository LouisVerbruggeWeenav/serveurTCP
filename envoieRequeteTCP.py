

import socket
import time


IP_VPS = '51.254.102.27'
PORT = 12345
server_address = (IP_VPS, PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(server_address)

for i in range(1400):
    message = f"Message {i+1} from Python client"
    client_socket.sendall(message.encode('utf-8'))
    if (i+1) % 20 == 0:  # Affiche un message tous les 20 envois
        print(f"Message {i+1} envoyé avec succès.")
    time.sleep(0.1)  # Pause pour éviter de surcharger le serveur

    
client_socket.close()
print("Tous les messages envoyés avec succès.")


"""
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP_VPS, 12345))  # Remplace par l'adresse de ton VPS
client.send("Salut serveur !".encode())
response = client.recv(1024).decode()
print(f"Réponse : {response}")
client.close()
"""