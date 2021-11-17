from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from psycopg2 import sql
from tools.token_tools import create_token

from tools.logging import logger

import bcrypt

def handle_request():
    logger.debug("Signup Handle Request")
    
    cur = g.db.cursor()
    #use data here to auth the user
    password_from_user_form = request.form['password']
    user = {
            "sub" : request.form['username'] #sub is used by pyJwt as the owner of the token
            }
    print(user['sub'])
    #sanitize the query
    query = sql.SQL("select {field} from {table} where {pkey} = %s").format(
      field=sql.Identifier('username'),
      table=sql.Identifier('users'),
      pkey=sql.Identifier('username'))
  
    cur.execute(query, (user['sub'],))
    result = cur.fetchone()
    print(result)
    if result is None:
        #salt pass
        salted_pwd = bcrypt.hashpw( bytes(password_from_user_form, 'utf-8'),  bcrypt.gensalt(12))
        #sanitize insert
        query = sql.SQL("insert into {table} ({first_field}, {second_field}) values (%s, %s);").format(
          table=sql.Identifier('users'),
          first_field=sql.Identifier('username'),
          second_field=sql.Identifier('password')
          )
        #execute
        cur.execute(query, (user['sub'], salted_pwd.decode('utf-8')))
        return json_response(message = "Successfully created account.")
    else:      
        return json_response(message = "Username already taken.")
