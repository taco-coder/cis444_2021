from flask import request, g, session
from flask_json import FlaskJSON, JsonError, json_response, as_json

from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Add to Cart Handle Request")
    if 'book_name' in session:
        session['book_name'] = session.get('book_name') + ";" + request.form['book_name'] 
    else:
        session['book_name'] = request.form['book_name']
    if 'book_price' in session:
        session['book_price'] = session.get('book_price') + ";" + request.form['book_price'] 
    else:
        session['book_price'] = request.form['book_price'] 


    return json_response( token = create_token( g.jwt_data ))