import random
from datetime import datetime

users = []
events = []
participations = []
reviews = []


def create_users(cursor):
    # Create 70 users
    user_count = 70
    CREATE_USERS_SQL = f"INSERT INTO users (username, password_hash, first_name, last_name, age, home_location) VALUES (%s, %s, %s, %s, %s, POINT%s);"

    first_names = [
        "James",
        "Michael",
        "Robert",
        "John",
        "David",
        "William",
        "Richard",
        "Joseph",
        "Thomas",
        "Christopher",
        "Mary",
        "Patricia",
        "Jennifer",
        "Linda",
        "Elizabeth",
        "Jessica",
        "Lisa",
    ]

    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Brown",
        "Jones",
        "Garcia",
        "Miller",
        "Davis",
        "Rodriguez",
        "Clarkson",
        "Graham",
        "Fraser",
        "Gordon",
    ]

    for i in range(user_count):
        # Define random user parameters
        username = f"user_{i}"
        password_hash = "MyRandomPasswordhash!"
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        age = random.randint(20, 60)
        home_location = (random.randint(-90, 90), random.randint(-180, 180))

        user = (
            username,
            password_hash,
            first_name,
            last_name,
            age,
            home_location,
        )
        users.append(user)

        cursor.execute(CREATE_USERS_SQL, user)


def create_past_events(cursor):
    # Create 10 events that happened in the past
    event_count = 10

    CREATE_EVENTS_SQL = f"INSERT INTO events (title, description, sport, intensity, skill_level, max_participants, location, event_creator, date_time) VALUES (%s, %s, %s, %s, %s, %s, POINT%s, %s, %s) RETURNING *;"

    sports = ["Football", "Basketball", "Hockey", "Boxing", "Golf"]
    intensity_list = ["Low", "Medium", "Intense"]
    skill_list = ["Beginner", "Intermediate", "Advanced"]

    for _ in range(event_count):
        sport = random.choice(sports)
        event_creator_tuple = random.choice(users)

        # "Andy's golf event!"
        title = f"{event_creator_tuple[0]}'s {sport} event!"
        description = "This is a placeholder description that is using extensive vocabulary as evident to populate the 100 minimum character count"

        intensity = random.choice(intensity_list)
        skill_level = random.choice(skill_list)
        max_participants = random.randint(5, 30)
        location = (random.randint(-90, 90), random.randint(-180, 180))

        # A date in the past, let's just use a random date from August 2024 with a random time between 8am and 8pm for example
        date_time = datetime(
            2024, 8, random.randint(1, 31), random.randint(8, 20), 0, 0
        )

        event = (
            title,
            description,
            sport,
            intensity,
            skill_level,
            max_participants,
            location,
            event_creator_tuple[0],  # username
            date_time,
        )

        cursor.execute(CREATE_EVENTS_SQL, event)
        full_event = cursor.fetchone()
        events.append(full_event)


def create_participations(cursor):
    # 1. Generate random number of participations for each event
    # 2. Find users to populate the event (i.e NOT the event creator, and NOT already in this event)

    SELECT_USERS = """SELECT * FROM users WHERE username != %s;"""

    INSERT_PARTICIPATION = """INSERT INTO user_event_participation (username, event_id, did_attend) VALUES (%s, %s, True);"""

    # 1.
    for event in events:
        # Max par. at index 6
        participant_count = random.randint(1, event[6])
        event_creator = event[8]

        cursor.execute(SELECT_USERS, (event_creator,))
        users_pool = cursor.fetchall()
        user_participants = []
        for i in range(participant_count):
            selected_user = random.choice(users_pool)
            if selected_user not in user_participants:
                user_participants.append(selected_user)

        for participant in user_participants:
            username = participant[0]
            event_id = event[0]
            cursor.execute(
                INSERT_PARTICIPATION,
                (
                    username,
                    event_id,
                ),
            )

            participations.append((username, event_id))


def create_reviews(cursor):
    INSERT_RATING_SQL = """INSERT INTO event_ratings (username, event_id, rating, title, review) VALUES (%s, %s, %s, %s, %s);"""

    for participation in participations:
        username = participation[0]
        event_id = participation[1]
        for e in events:
            if e[0] == event_id:
                event = e

        rating = random.randint(10, 50) / 10
        # user_2's football event review
        title = f"{username}'s {event[3]} event review"
        review = "This is a placeholder review that uses 60 characters, just about"
        rating_tuple = (username, event_id, rating, title, review)
        cursor.execute(INSERT_RATING_SQL, rating_tuple)
        reviews.append(rating_tuple)


def create_dummy_data(db_pool):
    # Create x amount of users
    # Create x amount of events
    conn = db_pool.getconn()
    with conn.cursor() as cursor:
        create_users(cursor=cursor)
        create_past_events(cursor=cursor)
        create_participations(cursor=cursor)
        create_reviews(cursor=cursor)
    conn.commit()
    db_pool.putconn(conn)
