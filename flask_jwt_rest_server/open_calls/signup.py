from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from psycopg2 import sql
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Signup Handle Request")
    
    cur = g.db.cursor()
    #use data here to auth the user
    password_from_user_form = request.form['password']
    user = {
            "sub" : request.form['username'] #sub is used by pyJwt as the owner of the token
            }
    #sanitize the query
    query = sql.SQL("select {field} from {table} where {pkey} = %s").format(
      field=sql.Identifier('username'),
      table=sql.Identifier('users'),
      pkey=sql.Identifier('username'))
  
    cur.execute(query, (user['sub'],))
    result = cur.fetchone()
    logger.debug("Result: " + result)
    if not user:
        return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )
    return json_response( token = create_token(user) , authenticated = False)