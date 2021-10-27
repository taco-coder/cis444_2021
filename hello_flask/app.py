from logging import exception
from flask import Flask,render_template,request, redirect, session
from flask import json
from flask.globals import current_app
from flask.json import jsonify
from flask_json import FlaskJSON, JsonError, json_response, as_json


import jwt
import datetime
import random
import bcrypt

from db_con import get_db_instance, get_db

app = Flask(__name__)
app.secret_key = "please don't hack my server"
FlaskJSON(app)

USER_PASSWORDS = { "cjardin": "strong password"}

IMGS_URL = {
            "DEV" : "/static",
            "INT" : "https://cis-444-fall-2021.s3.us-west-2.amazonaws.com/images",
            "PRD" : "http://d2cbuxq67vowa3.cloudfront.net/images"
            }

CUR_ENV = "PRD"

JWT_SECRET = None
CURRENT_USER = None

ACCOUNT_STATUS = None
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
@app.route('/prime_page')
def prime():
    try:
        if session['status'] == 'Create Account':
            return json_response(page="SignUpPage")
        elif session['status'] == 'Success':
            return json_response(page="AllBookPage")
        else:
            return json_response(page="LoginPage")
    except Exception as e:
        return json_response(page="LoginPage")

@app.route('/get_create_status')
def status():
    if ACCOUNT_STATUS == 2:
        return json_response(status = "Successfully created account.")
    elif ACCOUNT_STATUS == 1:
        return json_response(status = "Username already taken. Try another one.")
    return json_response(status="")

@app.route('/create_creds', methods=['POST', 'GET'])
def create_creds():
    cur = db.cursor()
    credsForm = request.form
    global ACCOUNT_STATUS
    cur.execute("select * from users where username = '" + jwt.encode({'username':credsForm['username']}, JWT_SECRET, algorithm="HS256") + "';")
    if cur.fetchone() is None:
        jwt_user = jwt.encode({'username':credsForm['username']}, JWT_SECRET, algorithm="HS256")
        salted_pwd = bcrypt.hashpw( bytes(credsForm['password'], 'utf-8'),  bcrypt.gensalt(12))
        cur.execute("insert into users (username, password) values ('" + jwt_user + "', '" + salted_pwd.decode('utf-8') + "');")
        db.commit()
        ACCOUNT_STATUS = 2
        session['status'] = 'Create Account'
        return redirect(request.referrer)
    else:
        ACCOUNT_STATUS = 1
        session['status'] = 'Create Account'
        return redirect(request.referrer)

@app.route('/check_creds', methods=['POST', 'GET'])
def check_creds():
    cur = db.cursor()
    global ACCOUNT_STATUS
    jwt_user = jwt.encode({'username':request.form['username']}, JWT_SECRET, algorithm="HS256")
    cur.execute("select * from users where username = '" + jwt_user + "';")
    if cur.fetchone() is None:
        session['status'] = 'Failed'
        ACCOUNT_STATUS = 3
        return redirect(request.referrer)
    else:
        cur.execute("select * from users where username = '" + jwt_user + "';")
        hashed_pass = cur.fetchone()[2]
        if bcrypt.checkpw(bytes(request.form['password'], 'utf-8'), bytes(hashed_pass, 'utf-8')):
            session['user'] = jwt_user
            session['status'] = 'Success'
            ACCOUNT_STATUS = None
            return redirect(request.referrer)
        else:
            session['status'] = 'Failed'
            ACCOUNT_STATUS = 3
            return redirect(request.referrer)

@app.route('/login_status')
def logStatus():
    if ACCOUNT_STATUS == 3:
        return json_response(login="Incorrect username/password. Please try again.")
    return json_response(login = "")

@app.route('/main_store')
def main_page():
    cur = db.cursor()
    cur.execute("select * from books;")
    db_books = cur.fetchall()
    return json_response(books = db_books)

@app.route('/logout')
def logout():
    session.clear() #clear all session info
    global ACCOUNT_STATUS
    ACCOUNT_STATUS = 0
    return redirect(request.referrer)

@app.route('/red_lepanka', methods=['GET'])    
def get_red_lepanka():
    cur = db.cursor()
    cur.execute("select * from books where id = 1;")
    bResult = cur.fetchone()
    cur.execute("select * from reviews where id = 1;")
    uReviews = cur.fetchall()
    return render_template("redlepanka.html", bookname=bResult[1], price=bResult[2], reviews=uReviews)

@app.route('/become_taco', methods=['GET'])    
def get_taco():
    cur = db.cursor()
    cur.execute("select * from books where id = 2;")    
    bResult = cur.fetchone()
    cur.execute("select * from reviews where id = 2;")
    uReviews = cur.fetchall()    
    return render_template("becomingtaco.html", bookname=bResult[1], price=bResult[2], reviews=uReviews)

@app.route('/car_jack', methods=['GET'])    
def get_carjack():
    cur = db.cursor()
    cur.execute("select * from books where id = 3;")    
    bResult = cur.fetchone()
    cur.execute("select * from reviews where id = 3;")
    uReviews = cur.fetchall()    
    return render_template("carjack.html", bookname=bResult[1], price=bResult[2], reviews=uReviews)

@app.route('/ego_bias', methods=['GET'])    
def get_ego_bias():
    cur = db.cursor()
    cur.execute("select * from books where id = 4;")
    bResult = cur.fetchone()
    cur.execute("select * from reviews where id = 4;")
    uReviews = cur.fetchall()    
    return render_template("ego.html", bookname=bResult[1], price=bResult[2], reviews=uReviews)

@app.route('/cart', methods=['GET'])    
def get_cart():
    try:
        cart_books = session['book_name'].split(";")
        cart_prices = session['book_price'].split(";")
        print(cart_books)
        print(cart_prices)
        return render_template("cart.html", books = cart_books, prices = cart_prices)
    except Exception as e:
        print("empty cart")
        return render_template("cart.html")

@app.route('/add_to_cart', methods=['POST', 'GET'])
def add_to_cart():
    if 'book_name' in session:
        session['book_name'] = session.get('book_name') + ";" + request.form['book_name'] 
    else:
        session['book_name'] = request.form['book_name']
    if 'book_price' in session:
        session['book_price'] = session.get('book_price') + ";" + request.form['book_price'] 
    else:
        session['book_price'] = request.form['book_price']        
    
    return redirect(request.referrer)

@app.route('/post_review', methods=['POST', 'GET'])
def post_review():
    cur = db.cursor()
    id = request.form['book_id']
    text = request.form.get('reviewtext')
    rate = request.form['rate']
    user = jwt.decode(session['user'], JWT_SECRET, algorithms=["HS256"])
    print(user)
    print(user['username'])
    cur.execute(f"insert into reviews (id, review, rating, review_user) values ( {id}, '{text}', {rate}, '{user['username']}');")
    db.commit()
    if int(request.form['book_id']) == 1:
        return get_red_lepanka()
    elif int(request.form['book_id']) == 2:
        return get_taco()
    elif int(request.form['book_id']) == 3:
        return get_carjack()
    else:
        return get_ego_bias()

app.run(host='0.0.0.0', port=80)
