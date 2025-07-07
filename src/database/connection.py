
import mysql.connector


class Connection:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database


    def cursor(self):
        # Crée une nouvelle connexion à chaque appel
        self.connect()
        return self.connection, self.connection.cursor()

    def connect(self):
        try: 
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("\033[92m Connection successful \033[0m")
            

        except mysql.connector.Error as err:
            print(f"\033[91m Error: {err} \033[0m")
            self.connection = None

    def disconnect(self):
        # Placeholder for disconnection logic
        print("Disconnecting from database")