import requests
import json
from pprint import pprint

API_KEY = "ah777687064604833763210903061553"

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
