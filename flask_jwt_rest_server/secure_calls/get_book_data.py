from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from psycopg2 import sql
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Get Books Data Handle Request")
    cur = g.db.cursor()
    #sanitize the query
    query = sql.SQL("select * from {table} where {pkey} = %s").format(
      table=sql.Identifier('books'),
      pkey=sql.Identifier('id'))
    
    cur.execute(query, (request.args.get('book_id', type=int), ) )
    print(cur.fetchone())
    return json_response( token = create_token(  g.jwt_data ) , info = {})