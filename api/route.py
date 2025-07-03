import flask
from flask import Flask, request
import pprint 

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/decryp')))
from decryp import decryp

fakeData = [
    {'timestamp': '1751456630.216411', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456630.259738', 'id': 419366912, 'length': '8', 'message': '0000000000000000'},
    {'timestamp': '1751456630.260359', 'id': 419366912, 'length': '8', 'message': '1101000000000000'},
    {'timestamp': '1751456630.316782', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456630.417131', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456630.517431', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456630.617748', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456630.718087', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456630.818546', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456630.918869', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456631.019279', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456631.119610', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456631.219908', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456631.255573', 'id': 419366912, 'length': '8', 'message': '1101000000000000'},
    {'timestamp': '1751456631.256365', 'id': 419366912, 'length': '8', 'message': '0000000000000000'},
    {'timestamp': '1751456631.320245', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456631.420612', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456631.520984', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456631.621329', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456631.721689', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456631.822022', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456631.922361', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456632.022700', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456632.123131', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456632.223512', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456632.251874', 'id': 419366912, 'length': '8', 'message': '1101000000000000'},
    {'timestamp': '1751456632.252675', 'id': 419366912, 'length': '8', 'message': '0000000000000000'},
    {'timestamp': '1751456632.323924', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456632.424226', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456632.524585', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456632.624980', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456632.725331', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456632.825660', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456632.926002', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456633.026341', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456633.126307', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456633.226506', 'id': 419366912, 'length': '8', 'message': '0019000103010401'},
    {'timestamp': '1751456633.248010', 'id': 419366912, 'length': '8', 'message': '1101000000000000'},
    {'timestamp': '1751456633.248825', 'id': 419366912, 'length': '8', 'message': '0000000000000000'},
    {'timestamp': '1751456633.326713', 'id': 419366912, 'length': '8', 'message': '0019000103010401'}
]

decryp(fakeData)


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
   print("Received request for home")
   dictionary = [{'Vehicle kkkkkkkkkkkkkkkk': [{'Status2': []},
              {'AC_Variables': []},
              {'Fault': []},
              {'Tst2': []},
              {'ACMaster': []},
              {'Status': []},
              {'DC_Variables': []},
              {'AC_Voltages': []},
              {'Temp': []},
              {'Internal': []},
              {'Tst1': []},
              {'SN': []},
              {'ACSlave': []}]},
 {'SELV': [{'SNS': []},
           {'Setup2': []},
           {'Setup1': []},
           {'APL_J1939': []},
           {'ACMaster': []},
           {'Control': []},
           {'V2XControl': []},
           {'ACSlave': []}]},
 {'Unknown': []}]
   return flask.jsonify(dictionary)

@app.route('/raspberry/data', methods=['POST'])
def raspberryData():
   if request.method == 'POST':
         data = flask.request.get_json()
         structData = data.get('structData') if data else None
         infoBoat = data.get('infoBoat') if data else None
         pprint.pprint(structData)
         pprint.pprint(infoBoat)
         print("=== Requête reçue ===")
         print(len(structData))

         content_length = request.content_length or 0
         headers_size = sum(len(k) + len(v) + 4 for k, v in request.headers.items())
         print(f"Taille headers : {headers_size} octets")
         print(f"Taille corps : {content_length} octets")

         decryp(structData)
         
         if data != None:
               return flask.jsonify({'data': 'datadata', 'success': True})
         else:
               return flask.jsonify({'data': 'datadata', 'success': False})


print("=== Flask démarre ===")
app.run(host='0.0.0.0', port=5000, debug=True)  # 51.254.102.27:5000
