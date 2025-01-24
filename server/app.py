# Imports
import os
from psycopg2 import pool
from flask import Flask, request
from dotenv import load_dotenv
from server.endpoints.events.delete_event import delete_event
from server.endpoints.reviews.create_review import create_review
from server.endpoints.reviews.get_reviews import get_reviews

# Auth
from .endpoints.auth.register import register_account
from .endpoints.auth.login import login

# Users
from .endpoints.users.user import get_user
from .endpoints.users.events import get_user_events
from .endpoints.users.last_event import get_user_last_event
from .endpoints.users.next_event import get_user_next_event
from .endpoints.users.recommended_events import recommended_events

# Events
from .endpoints.events.event_search import event_search
from server.endpoints.events.create_event import create_event
from server.endpoints.events.get_event_by_id import get_event_by_id
from server.endpoints.events.get_reviews_by_event_id import get_reviews_by_event_id
from server.endpoints.events.similar_events import get_similar_events

from .util.dummy_data import create_dummy_data
from .util.sql_statements import create_tables


# Loads the env file ready to be processed
load_dotenv()

# Fetches the value associated in the brackets from the .env file, a secure way of not including passwords in the code
database_password = os.getenv("DATABASE_PASSWORD")

# Create the API instance
app = Flask(__name__)

# Create a database connection pool
db_pool = pool.SimpleConnectionPool(
    1,  # minimum connections
    20,  # maximum connections
    database="proactive",
    user="postgres",
    password=database_password,
    host="127.0.0.1",
    port="5432",
)

# Create all tables on API startup, if they do not exist already
conn = db_pool.getconn()
with conn.cursor() as cursor:
    create_tables(cursor=cursor)
conn.commit()  # Commit changes
db_pool.putconn(conn)

# Auth


@app.post("/register")
def register_endpoint():
    return register_account(database_pool=db_pool)


@app.post("/login")
def login_endpoint():
    return login(database_pool=db_pool)


@app.get("/dummy-data")
def dummy_data():
    create_dummy_data(db_pool=db_pool)
    return "Ok", 200


# User
@app.get("/user/<username>")
def get_user_endpoint(username):
    return get_user(db_pool=db_pool, username=username)


@app.get("/user/<username>/events")
def get_user_events_endpoint(username):
    return get_user_events(db_pool=db_pool, username=username)


@app.get("/user/<username>/last-event")
def get_user_last_event_endpoint(username):
    return get_user_last_event(db_pool=db_pool, username=username)


@app.get("/user/<username>/next-event")
def get_user_next_event_endpoint(username):
    return get_user_next_event(db_pool=db_pool, username=username)


@app.get("/user/<username>/recommended-events")
def get_recommended_events_endpoint(username):
    # '/user/user_1/recommended-events/?amount=10'
    quantity = request.args.get("amount")

    return recommended_events(
        db_pool=db_pool, username=username, event_quantity=quantity
    )


# Events
@app.get("/events/search")
def get_event_search():
    # '/events/search/?username=johndoe123&query=hello+there'
    query = request.args.get("query")
    sort = request.args.get("sort")
    quantity = request.args.get("quantity")
    username = request.args.get("username")

    # Add specific filter parameters later

    return event_search(
        db_pool=db_pool,
        original_query=query,
        sort=sort,
        quantity=quantity,
        username=username,
    )


@app.get("/events/<event_id>")
def get_event(event_id):
    return get_event_by_id(db_pool=db_pool, event_id=event_id)


@app.get("/events/<event_id>/reviews")
def get_events_reviews(event_id):
    return get_reviews_by_event_id(db_pool=db_pool, event_id=event_id)


@app.get("/events/<event_id>/similar-events")
def get_similar_events_endpoint(event_id):
    # /events/<event_id>/similar-events?quantity=5
    quantity = request.args.get("quantity")
    return get_similar_events(db_pool=db_pool, event_id=event_id, quantity=quantity)


@app.post("/events")
def create_event_endpoint():
    return create_event(db_pool=db_pool)


@app.delete("/events/<event_id>")
def delete_event_endpoint(event_id):
    # /events/<event_id>?username=test
    username = request.args.get("username")
    return delete_event(db_pool=db_pool, event_id=event_id, username=username)


# Reviews
@app.get("/reviews")
def get_reviews_endpoint():
    # /reviews?username=test
    # /reviews?event_id=71
    # /reviews?username=test&event_id=71

    username = request.args.get("username")
    event_id = request.args.get("event_id")
    if username == None and event_id == None:
        return (
            "Request must contain atleast one 'username' or 'event_id' URL parameter",
            400,
        )

    return get_reviews(db_pool=db_pool, username=username, event_id=event_id)


@app.post("/reviews")
def create_review_endpoint():
    return create_review(db_pool=db_pool)
