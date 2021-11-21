from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Post Book Review Handle Request")

    cart = g.cart
    print(cart)
    cart.append({request.form.get('name') : request.form.get('price')})
    print(cart)
    g.cart = cart

    return json_response( token = create_token( g.jwt_data ), user_cart = cart )