from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from psycopg2 import sql
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Post Book Review Handle Request")
    cur = g.db.cursor()
    print(request.args.get('book_id'))
    print(request.args.get('review'))
    print(request.args.get('rate'))    
    return json_response( token = create_token(  g.jwt_data ) , books = {})