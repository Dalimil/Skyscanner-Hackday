from api import TripPricing, Optimizer, compute_flights
from pprint import pprint

if __name__ == "__main__":

	max_time = "2015-10-10T23:00:00"
	dest = "london"

	users = [
		{"origin":"lisbon","destination":dest,"arrival":max_time,"email":"@awdmkad"},
		{"origin":"edinburgh","destination":dest,"arrival":max_time,"email":"@awdm09809"}
	#	{"origin":"moscow","destination":dest,"arrival":max_time,"email":"@aw1231"},
	#	{"origin":"prague","destination":dest,"arrival":max_time,"email":"@awaaaaad"}
	]

	compute_flights(users)






