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

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        client_socket.close()
