import socket
import struct
from datetime import datetime

def extract_io_elements(io_data, counts, offset=0):
    io_dict = {}
    index = offset
    for size, count in counts.items():
        for _ in range(count):
            io_id = io_data[index]
            value = io_data[index + 1 : index + 1 + size]
            io_dict[io_id] = value
            index += 1 + size
    return io_dict

def decode_avl_packet(payload):
    codec_id = payload[0]
    record_count = payload[1]
    print(f"\n📦 Codec ID: {codec_id} | 📊 Records: {record_count}")

    index = 2  # après Codec ID et record count

    # --- pour simplifier, on traite un seul record (le 1er) ---
    timestamp = struct.unpack(">Q", payload[index:index+8])[0]
    dt = datetime.utcfromtimestamp(timestamp / 1000.0)
    index += 8

    priority = payload[index]
    index += 1

    lon = struct.unpack(">i", payload[index:index+4])[0] / 10_000_000
    lat = struct.unpack(">i", payload[index+4:index+8])[0] / 10_000_000
    index += 8

    altitude = struct.unpack(">H", payload[index:index+2])[0]
    angle = struct.unpack(">H", payload[index+2:index+4])[0]
    satellites = payload[index+4]
    speed = struct.unpack(">H", payload[index+5:index+7])[0]
    index += 7

    print(f"🕓 Timestamp: {dt}")
    print(f"📍 GPS: {lat}, {lon} | 🚗 Speed: {speed} km/h | 🛰 Sats: {satellites}")

    # IO elements
    event_io_id = payload[index]
    total_io_count = payload[index + 1]
    index += 2

    one_b = payload[index]
    index += 1
    one_b_data = payload[index:index + one_b * 2]
    index += one_b * 2

    two_b = payload[index]
    index += 1
    two_b_data = payload[index:index + two_b * 3]
    index += two_b * 3

    four_b = payload[index]
    index += 1
    four_b_data = payload[index:index + four_b * 5]
    index += four_b * 5

    eight_b = payload[index]
    index += 1
    eight_b_data = payload[index:index + eight_b * 9]
    index += eight_b * 9

    io_data = {}
    io_data.update(extract_io_elements(one_b_data, {1: one_b}))
    io_data.update(extract_io_elements(two_b_data, {2: two_b}))
    io_data.update(extract_io_elements(four_b_data, {4: four_b}))
    io_data.update(extract_io_elements(eight_b_data, {8: eight_b}))

    return dt, lat, lon, speed, io_data

def run_tcp_server(host='0.0.0.0', port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"✅ Serveur TCP FMC650 en écoute sur {host}:{port}...")

    while True:
        conn, addr = server.accept()
        print(f"\n📥 Connexion de {addr}")

        # Lire IMEI
        imei_data = conn.recv(1024)
        if len(imei_data) < 2:
            print("❌ Erreur : pas assez de données pour IMEI.")
            conn.close()
            continue

        imei_len = imei_data[1]
        imei = imei_data[2:2 + imei_len].decode(errors='ignore')
        print(f"📶 IMEI reçu : {imei}")

        conn.send(b'\x01')  # ACK

        # Lire données AVL
        data = conn.recv(4096)
        if not data or len(data) < 4:
            print("❌ Données AVL insuffisantes.")
            conn.close()
            continue

        avl_data_len = struct.unpack(">I", data[:4])[0]
        avl_payload = data[4:]  # exclure header TCP
        if len(avl_payload) < avl_data_len:
            print("❌ Données incomplètes, la taille réelle est inférieure à celle attendue.")
            conn.close()
            continue


        print(f"📐 Longueur AVL : {avl_data_len} octets")
        print(f"🧾 Données Codec 8 : {avl_payload.hex().upper()}")

        try:
            dt, lat, lon, speed, io = decode_avl_packet(avl_payload)

            if 500 in io:
                print(f"🟦 CAN IO ID 500 = {io[500].hex().upper()}")
            else:
                print("❌ Aucune donnée CAN (IO ID 500) trouvée.")

            # Réponse ACK (avec longueur)
            conn.send(struct.pack(">I", avl_data_len))

        except Exception as e:
            print(f"❗ Erreur de décodage : {e}")

        conn.close()

if __name__ == "__main__":
    run_tcp_server()
