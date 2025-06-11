import socket
# import mysql.connector
# from mysql.connector import Error
import threading


local_host = '0.0.0.0' 
local_port = 12345



# mysql_host = 'localhost'
# mysql_user = 'root'
# mysql_password = 'welcome1'
# mysql_database = 'fmc650_data'


# def insert_data_to_mysql(data):
#     try:
        
#         connection = mysql.connector.connect(
#             host=mysql_host,
#             user=mysql_user,
#             password=mysql_password,
#             database=mysql_database
#         )
        
#         if connection.is_connected():
#             cursor = connection.cursor()
#             query = "INSERT INTO can_data (data) VALUES (%s)"
#             cursor.execute(query, (data,))
#             connection.commit()
#             print(f"Data inserted into database: {data}")
#     except Error as e:
#         print(f"Error inserting data into MySQL: {e}")
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()


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
