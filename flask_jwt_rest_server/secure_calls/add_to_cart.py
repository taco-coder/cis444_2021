from flask import request, g, session
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Post Book Review Handle Request")

    if 'cart' in session:
      session['cart'] = session.get('cart') + ";" + {request.form.get('name') : request.form.get('price')}
    else:
      session['cart'] = {request.form.get('name') : request.form.get('price')}

    return json_response( token = create_token( g.jwt_data ), user_cart = session['cart'] )