
import json
from database.connection import Connection

import os
import pandas as pd4


from cantools.database.can.signal import NamedSignalValue



def make_json_serializable(obj):
    if isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(i) for i in obj]
    elif isinstance(obj, NamedSignalValue):
        return str(obj)  # ou obj.value si tu veux juste la valeur brute
    else:
        return obj


class Boat:
    def __init__(self, db):
        self.db = db
        if not isinstance(db, Connection):
            raise TypeError("\033[91m db must be an instance of Connection \033[0m")
        

    def add_boat(self, name, pathFile, dataStruct):
        # add to file
        # verify if the folder exists
        if not os.path.isdir(f"./api_rust/boats/{name}"):
            os.mkdir(f"./api_rust/boats/{name}")

        json_path = os.path.join(f"./api_rust/boats/{name}", f"{pathFile}.json")
        with open(json_path, "w") as f:
            dataStruct = make_json_serializable(dataStruct)
            json.dump(dataStruct, f)


        # add to database
        conn, mycursor = self.db.cursor()
        mycursor.execute("INSERT INTO boats (name, path) VALUES (%s, %s)", (name, pathFile))
        conn.commit()
        mycursor.close()
        conn.close()


    def get_all_requests(self):
        conn, mycursor = self.db.cursor()
        mycursor.execute("SELECT * FROM boats")
        result = mycursor.fetchall()
        mycursor.close()
        conn.close()
        if not result:
            raise ValueError("No boats found in the database")
        return result

    def get_boat_by_name(self, name):
        
        conn, mycursor = self.db.cursor()
        mycursor.execute("SELECT * FROM boats WHERE name = %s", (name,))
        result = mycursor.fetchall()
        mycursor.close()
        conn.close()
        if not result:
            return []   
        return result
    
    def get_boat_by_id(self, boat_id):
        conn, mycursor = self.db.cursor()
        mycursor.execute("SELECT id, name, path FROM boats WHERE id = %s", (boat_id,))
        result = mycursor.fetchall()
        mycursor.close()
        conn.close()
        if not result:
            return []
                
        return result[0]
    
    def get_grouped_boats(self):
        conn, mycursor = self.db.cursor()
        mycursor.execute("SELECT name, COUNT(name) FROM boats GROUP BY name")
        result = mycursor.fetchall()
        mycursor.close()
        conn.close()

        if not result:
            return []
                
        return result