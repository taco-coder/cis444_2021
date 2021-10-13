from flask import Flask,render_template,request
from flask_json import FlaskJSON, JsonError, json_response, as_json

import datetime
import random

app = Flask(__name__)
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"

@app.route('/') #endpoint
def index():
    return 'Web App with Python Caprice!' + USER_PASSWORDS['cjardin']

@app.route('/buy') #endpoint
def buy():
    return 'Buy'

@app.route('/hello') #endpoint
def hello():
    return render_template('hello.html',img_url=IMGS_URL[CUR_ENV] ) 

@app.route('/back',  methods=['GET']) #endpoint
def back():
    return render_template('backatu.html',input_from_browser=request.args.get('usay', default = "nothing", type = str) )

@app.route('/backp',  methods=['POST']) #endpoint
def backp():
    return render_template('backatu.html',input_from_browser= str(request.form) )


#Assigment 2
@app.route('/ss1', methods=['GET']) #endpoint
def ss1():
    return render_template('server_time.html', my_width = random.randint(100, 300),
                                               my_height = random.randint(100, 300), 
                                               rValue = random.randrange(0, 255), 
                                               gValue = random.randrange(0, 255), 
                                               bValue = random.randrange(0, 255),
                                               radius = random.randrange(0, 100))

#JSON stuff
@app.route('/get_time')
def get_time():
    return json_response(time=datetime.utcnow())

app.run(host='0.0.0.0', port=80)

