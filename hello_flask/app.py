from flask import Flask,render_template,request
from flask.globals import current_app
from flask_json import FlaskJSON, JsonError, json_response, as_json


import jwt
import datetime
import random

from db_con import get_db_instance, get_db

app = Flask(__name__)
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"

JWT_SECRET = None

db = get_db()

with open("mysecret", "r") as f:
    JWT_SECRET = f.read()

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
    return json_response(data={"serverTime":str(datetime.datetime.utcnow()),
                                "hello":"world my name isthaipehfaepouiha"
                                })

#JWT stuff
@app.route('/auth')                                
def get_auth():
    jwt_str = jwt.encode({"username" : "cary"}, JWT_SECRET, algorithm="HS256")
    return json_response(jwt = jwt_str)

@app.route('/expose')                                
def get_token():
    jwt_token = request.args.get('jwt')
    return json_response(output = jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"]))

#DB stuff
@app.route('/hello_db')                                
def hello_db():
    cur = db.cursor()
    cur.execute("select 5+5, 1+1, 3*9")
    first, second, third= cur.fetchone()
    return json_response(a = first, b = second, c = third)

#assignment 3 fullstack stuff
@app.route('/get_store')
def get_store():
    return render_template("bookstore.html")

@app.route('/get_signup', methods=['POST', 'GET'])
def get_signup():
    return render_template("signup.html")

@app.route('/check_signup')
def check_signup(value):
    if value is True:
        return render_template('signup.html', create_status="Successfully created new account.")
    else:
        return render_template('signup.html', create_status="This username is already taken. Try another one.")

@app.route('/create_creds', methods=['POST'])
def create_creds():
    cur = db.cursor()
    credsForm = request.form
    cur.execute("select * from users where username = '" + credsForm['username'] + "';")
    if cur.fetchone() is None:
        jwt_pass = jwt.encode({"password" :credsForm['password']}, JWT_SECRET, algorithm="HS256")
        cur.execute("insert into users (username, password) values ('" + credsForm['username'] + "', '" + jwt_pass + "');")
        db.commit()
        return check_signup(True)
    else:
        return check_signup(False)

@app.route('/check_creds', methods=['POST'])
def check_creds():
    cur = db.cursor()
    cur.execute("select * from users where username = '" + request.form['username'] + "';")
    if cur.fetchone() is None:
        return render_template("bookstore.html", account_status = "Incorrect username/password. Please try again.")
    else:
        cur.execute("select * from users where username = '" + request.form['username'] + "';")        
        jwt_pass = cur.fetchone()[2]
        decode_pass = jwt.decode(jwt_pass, JWT_SECRET, algorithms=["HS256"])
        if request.form['password'] == decode_pass['password']:
            return current_app.send_static_file("mainpage.html")
        else:
            return render_template("bookstore.html", account_status = "Incorrect username/password. Please try again.")

@app.route('/main_store')
def main_page():
    cur = db.cursor()
    cur.execute("select * from books;")
    books = cur.fetchall()
    return json_response(books = books)

@app.route('/red_lepanka', methods=['GET'])    
def get_red_lepanka():
    return render_template("redlepanka.html")

app.run(host='0.0.0.0', port=80)
