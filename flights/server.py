from flask import Flask, render_template, request
import json
from pprint import pprint
from api import TripPricing, Optimizer

server = Flask(__name__)


@server.route('/flights',methods=["POST"])
def flights():
	if request.method == "POST":
		print request.form.get("hello")
	return json.dumps({"hello":"not"})

server.run(port=8000, debug=True)