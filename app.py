import os
import sys
import urllib3
import lxml.html
from flask import Flask
from flask import Response
import json

app = Flask(__name__)
http = urllib3.PoolManager()
FLYBASE_URL = 'http://flybase.org/cgi-bin/quicksearch.cgi'

@app.route('/')
def root():
    return 'Welcome to the Flybase abbreviations proxy'

@app.route('/symbol/<symbol_id>')
def symbol(symbol_id):

	# DEBUG
	print symbol_id

	# make a POST request against flybase
	params = {
		'tab': 'dataType_tab',
		'species': 'Dmel',
		'field': 'SYM',
		'db': 'fbab',
		'caller': 'quicksearch',
		# 'context': 'Df(2L)ed50001'
		'context': symbol_id
	}
	response = http.request('POST', FLYBASE_URL, params)
	
	if response.status != 200:
		return 'The status code is ' + response.status
	else:
		# parse the response
		parsed_html = lxml.html.fromstring(response.data)

		# extract the necessary values from the response
		responded = False
		for tr in parsed_html.cssselect('div#content table#top_table>tbody>tr'):
			if tr.find('th').text == 'Sequence coordinates':
				responded = True

				coordinates = []
				for c in tr.cssselect('td>div>div.twocol_c_item_one'):
					coordinates.append(c.text)

				# origin = request.headers.get('Origin', '')
				response = Response(json.dumps({'coordinates': coordinates}), status=200, mimetype='application/json')
				# response.headers['Access-Control-Allow-Origin'] = origin
				# response.headers['Access-Control-Allow-Credentials'] = 'true'
				return response

	 	if not responded:
	 		return json.dumps({'coordinates': []})

if __name__ == "__main__":
    app.run()
	