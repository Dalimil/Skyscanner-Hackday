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


@server.route('/booking')
def success():
	xid = request.args.get('xid', '')
	s = """
	<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">

		<title>Booking</title>
		
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
		
		<script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.2.21/angular.min.js"></script>
	</head>
	
	<body>
		<div class="container" ng-app="MyApp">
			<div class="panel panel-primary" ng-controller="MyCtrl">
				<div class="panel-heading">
					<h2>Your booking</h2>
				</div>
				<table class="table">
					<tr ng-repeat="p in products">
						<td>
							<div class="pname">
								<h3 ng-bind="p.name"></h3>
							</div>
							<div class="row">
								<div class="col-md-4">
									<img src="{{p.image}}" class="product" style="max-height:240px"><br>
								</div>
								<div class="col-md-7" style="margin: 10px;" >
									<p ng-bind="p.description" style="color:gray"></p>
									<div class="buttonWrapper">
										<p>Book here with your friends as a group.</p>
										<a class="makeitsocial-button buttonNew" href="#" data-pid="{{p.xid}}"></a>
									</div>
								</div>
							</div>
						</td>
					</tr>
				</table>
				<div ng-show="!products.length" style="padding:10px 20px">
					You have no products, go to <a href="/admin.html">Admin page</a> to add your products.
				</div>
			</div>
		</div>
		
		<footer>
			<hr>
			<center>
				<p>Make Skyscanner Social Hackday 2015</p>
			</center>
		</footer>
	<script src="/papiclient.js"></script>
		
		<script>
			var app = angular.module('MyApp', ['papiclient']);
			app.controller('MyCtrl', ['$scope', 'PapiClient', function($scope, PapiClient){
				$scope.products = [];
				PapiClient.Products.getAll(function(data){
					if (data.error || !Array.isArray(data)){
						console.log('get products error:',data);
					} else {
						for(i=0;i<data.length;i++){
							if(data[i].xid == \""""+xid+"""\"){
								console.log("found");
								console.log(data[i]);
								$scope.products = [data[i]];
								break;
							}
						}
						/* $scope.products = data;*/
						setTimeout(function(){
							MiSnSpC.bindAll(); //set up mis button show
						}, 100);
					}
				});
			}]);
		</script>

		<script>
			var MiSnSpC = {
				purl: 'https://popup-sandbox.herokuapp.com'
			};
			(function(d,s,e){
				e=d.createElement("script");e.src=s;d.head.appendChild(e);
			})(document,"https://d21uq1a8lrig03.cloudfront.net/mplus.js");
		</script>

	</body>
</html>
	"""
	return s;