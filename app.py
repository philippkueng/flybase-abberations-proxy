import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def root():
    return 'Welcome to the Flybase abbreviations proxy'

@app.route('/symbol')
def symbol():
	return 'Here should be a symbol response'