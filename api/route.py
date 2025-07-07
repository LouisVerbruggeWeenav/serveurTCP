

import flask
from flask import Flask, request
import pprint 
import json



import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from decryp.decryp import decryp

from database.connection import Connection
from database.boat import Boat

from dotenv import dotenv_values, load_dotenv

load_dotenv()
dotenv = dotenv_values(".env")

# fakeData = [{'timestamp': '11:53:20', 'id': 419366912, 'length': '8', 'message': "b'\\x11\\x01\\x00\\x00\\x00\\x00\\x00\\x00'"}, {'timestamp': '11:53:20', 'id': 419366912, 'length': '8', 'message': "b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'"}, {'timestamp': '11:53:21', 'id': 419366912, 'length': '8', 'message': "b'\\x11\\x01\\x00\\x00\\x00\\x00\\x00\\x00'"}, {'timestamp': '11:53:21', 'id': 419366912, 'length': '8', 'message': "b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'"}, {'timestamp': '11:53:22', 'id': 419366912, 'length': '8', 'message': "b'\\x11\\x01\\x00\\x00\\x00\\x00\\x00\\x00'"}, {'timestamp': '11:53:22', 'id': 419366912, 'length': '8', 'message': "b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'"}, {'timestamp': '11:53:23', 'id': 419366912, 'length': '8', 'message': "b'\\x11\\x01\\x00\\x00\\x00\\x00\\x00\\x00'"}, {'timestamp': '11:53:23', 'id': 419366912, 'length': '8', 'message': "b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'"}, {'timestamp': '11:53:24', 'id': 419366912, 'length': '8', 'message': "b'\\x11\\x01\\x00\\x00\\x00\\x00\\x00\\x00'"}, {'timestamp': '11:53:24', 'id': 419366912, 'length': '8', 'message': "b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'"}, {'timestamp': '11:53:25', 'id': 419366912, 'length': '8', 'message': "b'\\x11\\x01\\x00\\x00\\x00\\x00\\x00\\x00'"}, {'timestamp': '11:53:25', 'id': 419366912, 'length': '8', 'message': "b'\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00'"}]
# print(decryp(fakeData))

# outputFake = [{'GARMIN': [{'OBC_MTA_Control (ID: 0x18FF0800)': [{'CtlStopCharge': [['ON', 'OFF', 'ON', 'OFF', 'ON', 'OFF', 'ON', 'OFF', 'ON', 'OFF', 'ON', 'OFF'], ['11:53:20', '11:53:20', '11:53:21', '11:53:21', '11:53:22', '11:53:22', '11:53:23', '11:53:23', '11:53:24', '11:53:24', '11:53:25', '11:53:25']]}, {'CtlRmode': [['OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF'], ['11:53:20', '11:53:20', '11:53:21', '11:53:21', '11:53:22', '11:53:22', '11:53:23', '11:53:23', '11:53:24', '11:53:24', '11:53:25', '11:53:25']]}, {'CtlCANEnable': [['OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF', 'OFF'], ['11:53:20', '11:53:20', '11:53:21', '11:53:21', '11:53:22', '11:53:22', '11:53:23', '11:53:23', '11:53:24', '11:53:24', '11:53:25', '11:53:25']]}, {'CtlIacMaxSet': [[0.1, 0.0, 0.1, 0.0, 0.1, 0.0, 0.1, 0.0, 0.1, 0.0, 0.1, 0.0], ['11:53:20', '11:53:20', '11:53:21', '11:53:21', '11:53:22', '11:53:22', '11:53:23', '11:53:23', '11:53:24', '11:53:24', '11:53:25', '11:53:25']]}, {'CtlVoutMaxSet': [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], ['11:53:20', '11:53:20', '11:53:21', '11:53:21', '11:53:22', '11:53:22', '11:53:23', '11:53:23', '11:53:24', '11:53:24', '11:53:25', '11:53:25']]}, {'CtlIoutMaxSet': [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], ['11:53:20', '11:53:20', '11:53:21', '11:53:21', '11:53:22', '11:53:22', '11:53:23', '11:53:23', '11:53:24', '11:53:24', '11:53:25', '11:53:25']]}]}]}]


print(dotenv)

database = Connection(
      host=dotenv.get("DB_HOST"),
      port=dotenv.get("DB_PORT"),
      user=dotenv.get("DB_USER"),
      password=dotenv.get("DB_PASSWORD"),
      database=dotenv.get("DB_NAME")
)

database.connect()
boat = Boat(database)


app = flask.Flask(__name__)
app.config["DEBUG"] = True


# testNAME = "test"

# boat.add_boat(testNAME, f"./boats/{testNAME}", outputFake)      
# 

#data = flask.request.get_json()
# boat_id = 5


# response = boat.get_boat_by_id(boat_id)
# print(f"name of boat: ")
# print(response)
# print("\n\n")



@app.route('/raspberry/data', methods=['POST'])
def raspberryData():
      if request.method == 'POST':
            data = flask.request.get_json()
            structData = data.get('structData') if data else None
            infoBoat = data.get('infoBoat') if data else None
            dataStruct = decryp(structData)
            print(infoBoat)
            print("=== Requête reçue ===")
            print(len(structData))

            content_length = request.content_length or 0
            headers_size = sum(len(k) + len(v) + 4 for k, v in request.headers.items())
            print(f"Taille headers : {headers_size} octets")
            print(f"Taille corps : {content_length} octets")
            print("=== Décryptage des données ===")
            print(infoBoat['name'])
            print(infoBoat['startRecord'])

            print("=== Ajout du bateau ===")
            boat.add_boat(infoBoat['name'], infoBoat['startRecord'], dataStruct)

            
            if data != None:
                  return flask.jsonify({'data': 'datadata', 'success': True})
            else:
                  return flask.jsonify({'data': 'datadata', 'success': False})



# api get all boats grouped by name
@app.route('/api/boats/grouped', methods=['GET'])
def get_grouped_boats():
      try:
            response = boat.get_grouped_boats()
            return flask.jsonify(response)
      except Exception as e:
            return flask.jsonify({"error": str(e)}), 500

# api select * from boats where name = 'Boat Name'
@app.route('/api/boats/by-name', methods=['POST'])
def get_boat_by_id_post():
      try:
            data = flask.request.get_json()
            boat_name = data.get('name') if data else None
            if not boat_name:
                  return flask.jsonify({"error": "Boat name is required"}), 400
            


            
            response = boat.get_boat_by_name(boat_name)
            print(f"voici la reponse")
            return flask.jsonify(response)
      except Exception as e:
            return flask.jsonify({"error": str(e)}), 500


@app.route('/api/boats/one', methods=['POST'])
def get_boat_one():
      try:
            data = flask.request.get_json()
            boat_id = data.get('id') if data else None
            if not boat_id:
                  return flask.jsonify({"error": "Boat name is required"}), 400

            print(boat_id)

            response = boat.get_boat_by_id(boat_id)
            print(f"name of boat: ")
            print(response)
            print("\n\n")

            

            with open(response[2], 'r') as f:
                  response = json.load(f)

            print("=== Boat data ===")
            print(response)
            pprint.pprint(response[0])

            return flask.jsonify(response[0])



            # response = main(response[3])
            # if isinstance(response, list):
            #       print('ok')
            #       response = {'data': response}

            # response = make_json_serializable(response)
            # print("ok 2")
            # return flask.jsonify(response)
    
      except Exception as e:
            print("flop")
            return flask.jsonify({"error": str(e)}), 500

print("=== Flask démarre ===")
app.run(host='0.0.0.0', port=5000)  # 51.254.102.27:5000