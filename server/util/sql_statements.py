# SQL code in a multi-line string
CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users(
    username VARCHAR(15) PRIMARY KEY,
    password_hash VARCHAR NOT NULL,
    access_level VARCHAR NOT NULL DEFAULT 'normal',
    first_name VARCHAR(25) NOT NULL,
    last_name VARCHAR(25) NOT NULL,
    age INTEGER NOT NULL,
    home_location POINT NOT NULL,


    CONSTRAINT min_username_length CHECK (LENGTH(username) >= 3),
    CONSTRAINT min_firstName_length CHECK (LENGTH(first_name) >= 2),
    CONSTRAINT min_lastName_length CHECK (LENGTH(last_name) >= 2),
    CONSTRAINT min_age CHECK (age >= 16),
    CONSTRAINT valid_coordinates CHECK (
        home_location[0] BETWEEN -90 AND 90 AND
        home_location[1] BETWEEN -180 AND 180
    )
);"""

CREATE_EVENTS_TABLE = """CREATE TABLE IF NOT EXISTS events(
    event_id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    sport VARCHAR NOT NULL,
    intensity VARCHAR NOT NULL,
    skill_level VARCHAR NOT NULL,
    max_participants INTEGER NOT NULL,
    location POINT,
    event_creator VARCHAR,
    date_time TIMESTAMP,

    FOREIGN KEY (event_creator) REFERENCES users(username)
    ON DELETE SET NULL,


    CONSTRAINT min_description_length CHECK (LENGTH(description) >= 100),
    CONSTRAINT max_participants_range CHECK (max_participants > 0 AND max_participants <= 50),
    CONSTRAINT valid_coordinates CHECK (
        location[0] BETWEEN -90 AND 90 AND
        location[1] BETWEEN -180 AND 180
    )
);"""

CREATE_EVENT_PARTICIPATION_TABLE = """CREATE TABLE IF NOT EXISTS user_event_participation(
    username VARCHAR NOT NULL,
    event_id INTEGER NOT NULL,
    did_attend BOOLEAN,

    PRIMARY KEY(username, event_id),
    FOREIGN KEY (username) REFERENCES users(username)
    ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
    ON DELETE CASCADE
);"""

CREATE_EVENT_RATINGS_TABLE = """CREATE TABLE IF NOT EXISTS event_ratings(
    username VARCHAR NOT NULL,
    event_id INTEGER NOT NULL,
    rating DECIMAL(2,1) NOT NULL,
    title VARCHAR NOT NULL,
    review VARCHAR NOT NULL,

    PRIMARY KEY (username, event_id),
    FOREIGN KEY (username) REFERENCES users(username)
    ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
    ON DELETE CASCADE,

    CONSTRAINT valid_rating CHECK (rating >= 1.0 AND rating <= 5.0),
    CONSTRAINT min_review_length CHECK (LENGTH(review) > 60)
);"""


def create_tables(cursor):
    cursor.execute(CREATE_USERS_TABLE)
    cursor.execute(CREATE_EVENTS_TABLE)
    cursor.execute(CREATE_EVENT_PARTICIPATION_TABLE)
    cursor.execute(CREATE_EVENT_RATINGS_TABLE)
