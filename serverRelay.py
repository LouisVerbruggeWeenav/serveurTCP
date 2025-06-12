import socket
import struct
from datetime import datetime

def extract_io_elements(io_data, counts, offset=0):
    """Parse IO elements and retourne un dict {io_id: value_bytes}"""
    io_dict = {}
    index = offset

    for size, count in counts.items():
        for _ in range(count):
            io_id = io_data[index]
            value = io_data[index + 1 : index + 1 + size]
            io_dict[io_id] = value
            index += 1 + size
    return io_dict

def decode_avl_packet(data):
    codec_id = data[4]
    record_count = data[5]

    print(f"\n📦 Codec ID: {codec_id} | 📊 Records: {record_count}")

    # Début du premier record
    index = 6

    timestamp = struct.unpack(">Q", data[index:index+8])[0]
    dt = datetime.utcfromtimestamp(timestamp / 1000.0)
    index += 8

    priority = data[index]
    index += 1

    # GPS
    lon = struct.unpack(">i", data[index:index+4])[0] / 10_000_000
    lat = struct.unpack(">i", data[index+4:index+8])[0] / 10_000_000
    index += 8

    altitude = struct.unpack(">H", data[index:index+2])[0]
    angle = struct.unpack(">H", data[index+2:index+4])[0]
    satellites = data[index+4]
    speed = struct.unpack(">H", data[index+5:index+7])[0]
    index += 7

    print(f"🕓 Timestamp: {dt}")
    print(f"📍 GPS: {lat}, {lon} | 🚗 Speed: {speed} km/h | 🛰 Sats: {satellites}")

    # IO Element section
    event_io_id = data[index]
    total_io_count = data[index + 1]
    index += 2

    one_b = data[index]
    index += 1
    one_b_data = data[index:index + one_b * 2]
    index += one_b * 2

    two_b = data[index]
    index += 1
    two_b_data = data[index:index + two_b * 3]
    index += two_b * 3

    four_b = data[index]
    index += 1
    four_b_data = data[index:index + four_b * 5]
    index += four_b * 5

    eight_b = data[index]
    index += 1
    eight_b_data = data[index:index + eight_b * 9]
    index += eight_b * 9

    # Reconstituer dictionnaire IO
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

        # --- Étape 1 : lire IMEI ---
        imei_data = conn.recv(1024)
        if len(imei_data) < 2:
            print("❌ Erreur : pas assez de données pour IMEI.")
            conn.close()
            continue

        imei_len = imei_data[1]
        imei = imei_data[2:2 + imei_len].decode(errors='ignore')
        print(f"📶 IMEI reçu : {imei}")

        # Réponse ACK : 0x01
        conn.send(b'\x01')

        # --- Étape 2 : lire le paquet Codec 8 ---
        data = conn.recv(2048)

        if not data:
            print("❌ Pas de données Codec.")
            conn.close()
            continue

        print(f"🧾 Données Codec 8 : {data.hex().upper()}")

        try:
            avl_data_len = struct.unpack(">I", data[0:4])[0]
            print(f"📐 Longueur AVL : {avl_data_len} octets")

            dt, lat, lon, speed, io = decode_avl_packet(data)

            if 500 in io:
                print(f"🟦 CAN IO ID 500 = {io[500].hex().upper()}")
            else:
                print("❌ Aucune donnée CAN (IO ID 500) trouvée.")

            # Répondre ACK
            conn.send(struct.pack(">I", avl_data_len))

        except Exception as e:
            print(f"❗ Erreur de décodage : {e}")

        conn.close()


if __name__ == "__main__":
    run_tcp_server()
