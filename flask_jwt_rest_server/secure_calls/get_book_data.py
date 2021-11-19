from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Get Books Data Handle Request")
    print(f"Book ID: {request.json['book_id']}")
    return json_response( token = create_token(  g.jwt_data ) , info = {})