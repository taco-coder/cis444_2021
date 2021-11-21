from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools import cart
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Post Book Review Handle Request")
    cart.add_to_cart({request.form['name']: request.form['price']})
    print(cart.get_cart())


    return json_response( token = create_token( g.jwt_data ), user_cart = cart.get_cart())