from flask import Flask, render_template, request

server = Flask(__name__, static_url_path='')

@server.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@server.route('/')
def main():
	return server.send_static_file('index.html')

@server.route('/admin')
def admin():
	return server.send_static_file('admin.html')

# json encoder for datetime
def isodatetime(obj):
	if hasattr(obj, 'isoformat'):
		return obj.isoformat()
	else:
		raise TypeError, 'Type %s with %s not JSON serialisable' % (type(obj), repr(obj))

# add endpoints for papi_python
import json
from papi import PapiClient

PREFIX = 'papi'
PROVIDERS = '/%s/providers' % PREFIX
PRODUCTS = '/%s/products' % PREFIX
PROVIDER = '%s/<id>' % PROVIDERS
PRODUCT = '%s/<id>' % PRODUCTS
PROVIDER_VALIDATOR = '%s/validate' % PROVIDERS
PRODUCT_VALIDATOR = '%s/validate' % PRODUCTS

papic = PapiClient()

from datetime import datetime
def json_datetime(obj):
	if isinstance(obj, datetime):
		return obj.isoformat()
	raise TypeError("Type %s not serializable" % type(obj))
	
@server.route(PROVIDERS, methods=['GET','POST'])
def providers():
	if request.method == 'GET':
		ps = papic.get_providers()
		return json.dumps(ps, default=json_datetime)
	else:
		data = request.get_json()
		r = papic.post_provider(data)
		return json.dumps(r)

@server.route(PROVIDER, methods=['GET','PUT','DELETE'])
def provider(id):
	if request.method == 'GET':
		p = papic.get_provider_by_id(id)
		return json.dumps(p, default=json_datetime)
	elif request.method == 'PUT':
		data = request.get_json()
		r = papic.put_provider_by_id(id, data)
		return json.dumps(r)
	else:
		r = papic.delete_provider_by_id(id)
		return json.dumps(r)

@server.route(PROVIDER_VALIDATOR, methods=['POST'])
def provider_validate():
	data = request.get_json()
	if not data:
		return '{"error":"no data given"}'
	r = papic.post_validate_provider(data)
	return json.dumps(r, default=json_datetime)

@server.route(PRODUCTS, methods=['GET','POST'])
def products():
	if request.method == 'GET':
		ps = papic.get_products()
		return json.dumps(ps, default=json_datetime)
	else:
		data = request.get_json()
		r = papic.post_product(data)
		return json.dumps(r)

@server.route(PRODUCT, methods=['GET','PUT','DELETE'])
def product(id):
	if request.method == 'GET':
		p = papic.get_product_by_id(id)
		return json.dumps(p, default=json_datetime)
	elif request.method == 'PUT':
		data = request.get_json()
		r = papic.put_product_by_id(id, data)
		return json.dumps(r)
	else:
		r = papic.delete_product_by_id(id)
		return json.dumps(r)

@server.route(PRODUCT_VALIDATOR, methods=['POST'])
def product_validate():
	data = request.get_json()
	if not data:
		return '{"error":"no data given"}'
	r = papic.post_validate_product(data)
	return json.dumps(r, default=json_datetime)
