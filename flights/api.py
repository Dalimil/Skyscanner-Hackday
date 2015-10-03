import requests
import json
from pprint import pprint
import time
import calendar
import math

API_KEY = "ah777687064604833763210903061553"

PLACE_ID_CODES = {
	"edinburgh":"EDI-sky",
	"paris":"PARI-sky",
	"london":"LOND-sky",
	"prague":"PRG-sky",
	"lisbon":"LIS-sky",
	"madrid":"MAD-sky",
	"rome":"ROME-sky",
	"bern":"BRN-sky",
	"zagreb":"ZAG-sky",
	"kiev":"KIEV-sky",
	"berlin":"BERL-sky",
	"munich":"MUC-sky",
	"warsow":"WARS-sky",
	"stockholm":"STOC-sky",
	"moscow":"MOSC-sky",
	"dubai":"DXBA-sky",
	"beijing":"BJSA-sky",
	"new york":"NYCA-sky",
	"nyc":"NYCA-sky",
	"boston":"BOS-sky",
	"dublin":"DUB-sky"
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

class Optimizer:
	def __init__(self, trips):
		self.trips = [trip.summary for trip in trips]
		self.state = [0]*len(self.trips)

	def get_price_measure(self, state):
		return sum([100.0*float(trip[s]["Price"])/trip[0]["Price"] for s, trip in zip(state, self.trips)])

	def get_time_measure(self, state):
		times = [calendar.timegm(time.strptime(trip[s]["Arrival"],"%Y-%m-%dT%H:%M:%S"))/60.0 for s,trip in zip(state,self.trips)]

		average = sum(times)/len(times)
		variance = math.pow(sum([(t-average)**2 for t in times]),0.5)

		return variance

	def cost(self, state):
		return self.get_price_measure(state) + self.get_time_measure(state)

	def optimize(self):
		best_cost = self.cost(self.state)
		best_state = list(self.state)

		p=True
		while p:
			p=False
			for i in range(len(self.state)):
				new_state = list(best_state)

				if self.state[i] == 0:
					new_state[i] += 1
					new_cost = self.cost(new_state)

					if new_cost < best_cost:
						best_cost = new_cost
						best_state = list(new_state)
						p=True

				elif self.state[i] == len(self.trips[i])-1:
					new_state[i] -= 1
					new_cost = self.cost(new_state)

					if new_cost < best_cost:
						best_cost = new_cost
						best_state = list(new_state)
						p=True

				else:
					new_state[i] += 1
					new_cost = self.cost(new_state)

					if new_cost < best_cost:
						best_cost = new_cost
						best_state = list(new_state)
						p=True

					new_state[i] -= 2
					new_cost = self.cost(new_state)

					if new_cost < best_cost:
						best_cost = new_cost
						best_state = list(new_state)
						p=True

		return best_state


class TripPricing:
	def __init__(self, origin, destination, max_arrival_time_str):
		self.API_KEY = "ah777687064604833763210903061553"
		self.CREATE_SESSION_URL = "http://partners.api.skyscanner.net/apiservices/pricing/v1.0"
		self.POLL_SESSION_URL = ""

		self.max_arrival_time = time.strptime(max_arrival_time_str,"%d/%m/%Y %H:%M")
		self.origin_place_id = PLACE_ID_CODES[origin.strip().lower()]
		self.destination_place_id = PLACE_ID_CODES[destination.strip().lower()]

		self.flights = {}
		self.summary = []

	def format_and_save_poll_data(self,data):
		carriers = { item["Id"]:item for item in data["Carriers"]}
		segments = { item["Id"]:item for item in data["Segments"]}
		legs = { item["Id"]: item for item in data["Legs"] if time.strptime(item["Arrival"],"%Y-%m-%dT%H:%M:%S") < self.max_arrival_time}
		itineraries = { item["OutboundLegId"]: {
			"OutboundLegId":item["OutboundLegId"],
			"Pricing":item["PricingOptions"][0],
			"BookingDetailsLink":item["BookingDetailsLink"]
		} for item in data["Itineraries"] if item["OutboundLegId"] in legs}

		self.flights["Carriers"] = carriers
		self.flights["Segments"] = segments
		self.flights["Legs"] = legs
		self.flights["Itineraries"] = itineraries

	def create_summary(self,flights):
		self.summary = sorted([{
			"Id": _id,
			"Duration":self.flights["Legs"][itinerary["OutboundLegId"]]["Duration"],
			"Arrival":self.flights["Legs"][itinerary["OutboundLegId"]]["Arrival"],
			"Price":itinerary["Pricing"]["Price"]
		} for _id, itinerary in self.flights["Itineraries"].items()], key=lambda x: x["Price"])

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
			print "Polling successful."
			data = json.loads(r.text)

			self.format_and_save_poll_data(data)

			self.create_summary(self.flights)
			


