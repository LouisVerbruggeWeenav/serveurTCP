import flask


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





print("=== Flask démarre ===")
app.run(host='0.0.0.0', port=5000, debug=True)  # 51.254.102.27:5000
