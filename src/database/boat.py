
import json
from database.connection import Connection

import os
import pandas as pd


class Boat:
    def __init__(self, db):
        self.db = db
        if not isinstance(db, Connection):
            raise TypeError("\033[91m db must be an instance of Connection \033[0m")
        

    def add_boat(self, name, path, dataStruct):
        # add to file
        # verify if the folder exists
        if not os.path.isdir(f"./boats/{name}"):
            os.mkdir(f"./boats/{name}")

        # add file to the folder
        # convert dataStruct to a DataFrame
        json_path = os.path.join(f"./boats/{name}", f"{name}.json")
        with open(json_path, "w") as f:
            json.dump(dataStruct, f)


        # add to database
        conn, mycursor = self.db.cursor()
        mycursor.execute("INSERT INTO boats (name, path) VALUES (%s, %s)", (name, path))
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
        mycursor.execute("SELECT * FROM boats WHERE id = %s", (boat_id,))
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