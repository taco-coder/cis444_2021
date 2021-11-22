from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from psycopg2 import sql
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("One Click Buy Handle Request")
    db = g.db
    cur = db.cursor()
    bName = request.form['name']
    bPrice = request.form['price']
    user = g.jwt_data
    query = sql.SQL("insert into {table} ({name}, {price}, {user}) values (%s, %s, %s);").format(
        table=sql.Identifier('orders'),
        name=sql.Identifier('bookname'),
        price=sql.Identifier('bookprice'),
        user=sql.Identifier('username')
    )    
    cur.execute(query, (bName, bPrice, user))

    return json_response( token = create_token( user ), info = {'name' : bName, 'price': bPrice, 'user': user})