from flask import request


def create_event(db_pool):
    # We need to recieve the following data in the request body:
    # title, description, sport,
    # intensity, skill level, max participants,
    # location, event creator, date time
    data = request.get_json()
    print(type(data))

    # Validate data before sending to database
    if data["max_participants"] > 50 or data["max_participants"] <= 0:
        issue = "Max participants must be between 1 and 50 inclusive"

    elif len(data["description"]) < 100:
        issue = "Description must be atleast 100 characters"

    elif abs(data["location"][0]) > 90:
        issue = "Invalid latitude!"

    elif abs(data["location"][1]) > 180:
        issue = "Invalid longitude!"
    else:
        issue = None

    if issue:
        return issue, 400

    INSERT_EVENT_SQL = "INSERT INTO events (title, description, sport, intensity, skill_level, max_participants, location, event_creator, date_time) VALUES (%s, %s, %s, %s, %s, %s, POINT%s, %s, %s);"

    conn = db_pool.getconn()
    cursor = conn.cursor()

    try:
        new_event_tuple = (
            data["title"],
            data["description"],
            data["sport"],
            data["intensity"],
            data["skill_level"],
            data["max_participants"],
            (data["location"][0], data["location"][1]),
            data["event_creator"],
            data["date_time"],
        )
        cursor.execute(INSERT_EVENT_SQL, new_event_tuple)
        conn.commit()
    except Exception as error:
        print(error)
        return "There was an error whilst trying to create the event", 500
    finally:
        db_pool.putconn(conn)
    return "", 201
