import socket
# import mysql.connector
# from mysql.connector import Error
import threading


local_host = '0.0.0.0' 
local_port = 12345


import struct

def parse_avl_packet(data):
    # Skip first 4 bytes
    avl_length = int.from_bytes(data[4:8], byteorder='big')
    codec_id = data[8]
    record_count = data[9]
    
    print(f"📦 AVL length: {avl_length}")
    print(f"🧬 Codec ID: {codec_id}")
    print(f"📄 Number of Records: {record_count}")
    
    offset = 10
    for i in range(record_count):
        timestamp = int.from_bytes(data[offset:offset+8], byteorder='big')
        priority = data[offset+8]
        lon = struct.unpack('>i', data[offset+9:offset+13])[0] / 10000000
        lat = struct.unpack('>i', data[offset+13:offset+17])[0] / 10000000
        alt = struct.unpack('>h', data[offset+17:offset+19])[0]
        angle = struct.unpack('>h', data[offset+19:offset+21])[0]
        satellites = data[offset+21]
        speed = struct.unpack('>H', data[offset+22:offset+24])[0]

        print(f"\n🔸 Record #{i+1}:")
        print(f"🕒 Timestamp: {timestamp}")
        print(f"📍 Position: ({lat}, {lon})")
        print(f"📶 Satellites: {satellites}")
        print(f"🛣️ Speed: {speed} km/h")
        print(f"📐 Angle: {angle}° | Altitude: {alt} m")

        # Advance offset to skip the rest (we ignore IO for now)
        offset += 60  # approx. for demo – you can parse IO elements properly after





def handle_client(client_socket):
    try:
        data = client_socket.recv(4096)
        if not data:
            print("Client disconnected.")
            return

        print(f"Données brutes : {data}")

        # Extraire la longueur de l’IMEI
        imei_len = int.from_bytes(data[0:2], byteorder='big')
        imei = data[2:2+imei_len].decode()
        print(f"IMEI : {imei}")

        # Envoyer l’ACK requis
        client_socket.send(b'\x01')
        print("ACK envoyé au traceur")

        # Ensuite, il peut envoyer des paquets AVL (données GPS, etc.)
        while True:
            avl_data = client_socket.recv(4096)
            if not avl_data:
                print("Client disconnected après IMEI.")
                break
            print(f"AVL data reçue : {avl_data}")
            parse_avl_packet(avl_data)

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        client_socket.close()



def start_tcp_server():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((local_host, local_port))
    server_socket.listen(5)
    print(f"Serveur TCP en écoute sur {local_host}:{local_port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connexion acceptée de {client_address}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == '__main__':
    start_tcp_server()
