from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from psycopg2 import sql
from tools.token_tools import create_token

from tools.logging import logger

import bcrypt

def handle_request():
    logger.debug("Login Handle Request")
    db = g.db
    cur = db.cursor()
    #use data here to auth the user
    password_from_user_form = request.form['password']
    user = {
            "sub" : request.form['username'] #sub is used by pyJwt as the owner of the token
            }
    #sanitize the query
    query = sql.SQL("select * from {table} where {pkey} = %s").format(
      table=sql.Identifier('users'),
      pkey=sql.Identifier('username'))
    
    #check if user exists
    cur.execute(query, (user['sub'],))     
    if not cur.fetchone():
        return json_response(message = "Incorrect username/password. Please try again.", authenticated = False)
    else:
        #get user row
        cur.execute(query, (user['sub'],))
        #get pass from row
        hashed_pass = cur.fetchone()[2]
        
        if bcrypt.checkpw(bytes(password_from_user_form, 'utf-8'), bytes(hashed_pass, 'utf-8')):
            g.cart = {}
            return json_response( token = create_token(user) , authenticated = True)
        else:
            return json_response(message = "Incorrect username/password. Please try again.", authenticated = False)

