import os
import urllib3
import lxml.html
from flask import Flask

app = Flask(__name__)
http = urllib3.PoolManager()
FLYBASE_URL = 'http://flybase.org/cgi-bin/quicksearch.cgi'

@app.route('/')
def root():
    return 'Welcome to the Flybase abbreviations proxy'

@app.route('/symbol')
def symbol():

	# make a POST request against flybase
	params = {
		'tab': 'dataType_tab',
		'species': 'Dmel',
		'field': 'SYM',
		'db': 'fbab',
		'caller': 'quicksearch',
		# 'context': 'Df(2L)net3'
		'context': 'Df(2L)ed50001'
	}
	response = http.request('POST', FLYBASE_URL, params)
	
	if response.status != 200:
		return 'The status code is ' + response.status
	else:
		# parse the response
		parsed_html = lxml.html.fromstring(response.data)

		# extract the necessary values from the response

		return response.data

	
	
	# respond to this request
	