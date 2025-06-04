from flask import Flask, jsonify
from ssh_telnet import fetch_port_descriptions
from dotenv import load_dotenv
from flask_cors import CORS
import os
load_dotenv()


app = Flask(__name__)
CORS(app)
@app.route("/ports")
def get_ports():
    result = fetch_port_descriptions()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5008)
