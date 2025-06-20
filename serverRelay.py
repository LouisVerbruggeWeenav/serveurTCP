import flask


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
   print("Received request for home")
   dictionary = [{'Vehicle': [{'Status2': []},
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
app.run(debug=True, use_reloader=False) # http://127.0.0.1:5000/
