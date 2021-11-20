from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from psycopg2 import sql
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Post Book Review Handle Request")
    user = g.jwt_data
    print(request.form.get('book_id'))
    print(request.form.get('review'))
    print(request.form.get('rate'))
    print(user)    
    return json_response( token = create_token(  user ) , books = {"id": request.args.get('book_id'), "review": request.args.get('review'), "rate": request.args.get('rate')})