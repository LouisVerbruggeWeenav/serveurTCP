

import flask
from flask import Flask, request
import pprint 



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

            print("=== Ajout du bateau ===")
            boat.add_boat(infoBoat['name'], f"./boats/{infoBoat['name']}", dataStruct)

            
            if data != None:
                  return flask.jsonify({'data': 'datadata', 'success': True})
            else:
                  return flask.jsonify({'data': 'datadata', 'success': False})



print("=== Flask démarre ===")
app.run(host='0.0.0.0', port=5000)  # 51.254.102.27:5000
