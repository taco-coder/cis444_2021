from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user
    cur = g.db.cursor()
    password_from_user_form = request.form['password']
    user = {
            "sub" : request.form['firstname'] #sub is used by pyJwt as the owner of the token
            }
    if not user:
        return json_response(status_ = 401, message = 'Invalid credentials', authenticated =  False )
    
    cur.execute(f"select * from users where username = '{user}';")

    return json_response( token = create_token(user) , authenticated = False)