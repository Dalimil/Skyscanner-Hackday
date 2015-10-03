import requests
import json
from pprint import pprint
import time

API_KEY = "ah777687064604833763210903061553"

PLACE_ID_CODES = {
	"edinburgh":"EDI-sky",
	"paris":"PARI-sky",
	"london":"LOND-sky",
	"prague":"PRG-sky",
	"lisbon":"LIS-sky"
}

def get_place_id(city):

	url = "http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/GB/EUR/en-GB"
	headers = {
		"Accept":"application/json"
	}
	params = {
		"query":city,
		"apiKey":API_KEY
	}

	r = requests.get(url, headers=headers, params=params)

	return r


def create_session():

	url = "http://partners.api.skyscanner.net/apiservices/pricing/v1.0"
	headers = {
		"Content-Type":"application/x-www-form-urlencoded",
		"Accept":"application/json"
	}
	data = {
		"apiKey":API_KEY,
		"country":"GB",
		"currency":"GBP",
		"locale":"en",
		"originplace":"EDI-sky",
		"destinationplace":"PARI-sky",
		"outbounddate":"2015-10-10"
	}

	r = requests.post(url, headers=headers, data=data)

	return r

def poll_session(session_url):

	url = session_url
	headers = {
		"Accept":"application/json"
	}
	params = {
		"apiKey":API_KEY
	}

	r = requests.get(url, headers=headers, params=params)

	return r

class TripPricing:
	def __init__(self, origin, destination, max_arrival_time_str):
		self.API_KEY = "ah777687064604833763210903061553"
		self.CREATE_SESSION_URL = "http://partners.api.skyscanner.net/apiservices/pricing/v1.0"
		self.POLL_SESSION_URL = ""

		self.max_arrival_time = time.strptime(max_arrival_time_str,"%d/%m/%Y %H:%M")
		self.origin_place_id = PLACE_ID_CODES[origin.strip().lower()]
		self.destination_place_id = PLACE_ID_CODES[destination.strip().lower()]

		self.flights = {}

	def format_and_save_poll_data(self,data):
		carriers = { item["Id"]:item for item in data["Carriers"]}
		segments = { item["Id"]:item for item in data["Segments"]}
		legs = { item["Id"]: item for item in data["Legs"]}
		itineraries = [{
			"OutboundLegId":obj["OutboundLegId"],
			"Pricing":obj["PricingOptions"][0],
			"BookingDetailsLink":obj["BookingDetailsLink"]
		} for obj in data["Itineraries"]]

		self.flights["Carriers"] = carriers
		self.flights["Segments"] = segments
		self.flights["Legs"] = legs
		self.flights["Itineraries"] = itineraries

	def open_session(self):
		headers = {
			"Content-Type":"application/x-www-form-urlencoded",
			"Accept":"application/json"
		}
		data = {
			"apiKey":self.API_KEY,
			"country":"GB",
			"currency":"EUR",
			"locale":"en",
			"originplace":self.origin_place_id,
			"destinationplace":self.destination_place_id,
			"outbounddate":time.strftime("%Y-%m-%d",self.max_arrival_time)
		}

		r = requests.post(self.CREATE_SESSION_URL, headers=headers, data=data)

		if r.status_code in [200,201]:
			self.POLL_SESSION_URL = r.headers["location"]

	def poll_session(self):

		if not self.POLL_SESSION_URL:
			return "No session active."

		headers = {
			"Accept":"application/json"
		}
		params = {
			"apiKey":self.API_KEY,
			"sorttype":"price",
			"sortorder":"asc"
		}

		r = requests.get(self.POLL_SESSION_URL, headers=headers, params=params)

		if r.status_code in [200,201]:
			print "request successful"
			data = json.loads(r.text)

			self.format_and_save_poll_data(data)

						

			


