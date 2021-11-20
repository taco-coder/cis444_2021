from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from psycopg2 import sql
from tools.token_tools import create_token

from tools.logging import logger

def handle_request():
    logger.debug("Post Book Review Handle Request")
    db = g.db
    cur = db.cursor()
    #init variables
    user = g.jwt_data
    bid = request.form.get('book_id')
    user_review = request.form.get('review')
    user_rate = request.form.get('rate')
    
    #sanitize the query to insert new book review
    query = sql.SQL("insert into {table} ({id}, {review}, {rating}, {review_user}) values (%i, %s, %i, %s)").format(
      table=sql.Identifier('reviews'),
      id=sql.Identifier('id'),
      review=sql.Identifier('review'),
      rating=sql.Identifier('rating'),
      review_user=sql.Identifier('review_user'))
    
    cur.execute(query, (bid, user_review, user_rate, user,))
    db.commit()
    return json_response( token = create_token(  user ) , review = {"user": user['sub'], "review":user_review, "rate": user_rate})