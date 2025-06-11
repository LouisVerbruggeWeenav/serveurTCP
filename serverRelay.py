import socket
# import mysql.connector
# from mysql.connector import Error
import threading


local_host = '127.0.0.1' 
local_port = 5000 



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
    while True:
        try:
            
            data = client_socket.recv(4096)
            if not data:
                print("Client disconnected.")
                break

            print(data)


            # insert_data_to_mysql(data)

        except Exception as e:
            print(f"Error receiving data: {e}")
            break

    client_socket.close()


def start_tcp_server():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
