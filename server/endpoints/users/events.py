import json

from server.util.haversine import calculate_haversine_distance

# GET USER'S EVENTS

from ...util.format_conversion import format_event_tuple_to_dict


def get_user_events(db_pool, username):
    # list of dictionaries
    # [{"created_by_me": False, "upcoming": False, "events": [{...}]}, (Events i have participated in the past)
    # {"created_by_me": True, "upcoming": False, "events": [{...}]}, (Events i have hosted in the past)
    # {"created_by_me": False, "upcoming": True, "events": [{...}]}, (Events i am participating in, in the future)
    # {"created_by_me": True, "upcoming": True, "events": [{...}]}] (Events i am hosting in the future)
    # Each event will be a dictionary

    PARTICIPATED_PAST_SQL = """SELECT events.* FROM user_event_participation INNER JOIN events ON user_event_participation.event_id = events.event_id WHERE user_event_participation.username = %s AND events.date_time < NOW();"""

    CREATED_PAST_SQL = (
        "SELECT * FROM events WHERE event_creator = %s AND date_time < NOW();"
    )

    PARTICIPATING_FUTURE_SQL = """SELECT events.* FROM user_event_participation INNER JOIN events ON user_event_participation.event_id = events.event_id WHERE user_event_participation.username = %s AND events.date_time > NOW();"""

    CREATED_FUTURE_SQL = (
        "SELECT * FROM events WHERE event_creator = %s AND date_time > NOW();"
    )

    GET_USERS_LOCATION_SQL = """SELECT home_location FROM users WHERE username = %s;"""

    GET_NUMER_OF_PARTICIPANTS_SQL = (
        """SELECT COUNT(event_id) FROM user_event_participation WHERE event_id = %s;"""
    )

    conn = db_pool.getconn()
    cursor = conn.cursor()
    try:
        # Participated, in the past
        cursor.execute(PARTICIPATED_PAST_SQL, (username,))
        participated_past_result = cursor.fetchall()

        # Created by me, in the past
        cursor.execute(CREATED_PAST_SQL, (username,))
        created_by_me_past_result = cursor.fetchall()

        # Participating, in the future
        cursor.execute(PARTICIPATING_FUTURE_SQL, (username,))
        participating_future_result = cursor.fetchall()

        # Created by me, in the future
        cursor.execute(CREATED_FUTURE_SQL, (username,))
        created_by_me_future_result = cursor.fetchall()

    except Exception as error:
        print("Something went wrong with fetching events")
        print(error)

        return "There was an unexpected error", 500
    finally:
        db_pool.putconn(conn)

    # Result is an array of event tuples.
    # we can see which values correspond to the event
    # by viewing the contents of result

    # Format the past participated events into this array
    formatted_participated_past_result = []

    for event in participated_past_result:
        event_dict = format_event_tuple_to_dict(event_tuple=event)

        cursor.execute(GET_NUMER_OF_PARTICIPANTS_SQL, (event_dict["event_id"],))
        participant_count = cursor.fetchone()

        event_dict["participant_count"] = participant_count[0]

        cursor.execute(GET_USERS_LOCATION_SQL, (username,))
        home_location = cursor.fetchone()[0]
        # Calculate haversine distance between user and event
        distance = calculate_haversine_distance(
            eval(home_location), event_dict["location"]
        )
        # Round the distance to 1 decimal
        distance = round(distance, 1)
        event_dict["distance_from_home_km"] = distance

        formatted_participated_past_result.append(event_dict)

    # Format the past created events into this array
    formatted_created_events_result = []

    for event in created_by_me_past_result:
        event_dict = format_event_tuple_to_dict(event_tuple=event)

        cursor.execute(GET_USERS_LOCATION_SQL, (username,))
        home_location = cursor.fetchone()[0]

        cursor.execute(GET_NUMER_OF_PARTICIPANTS_SQL, (event_dict["event_id"],))
        participant_count = cursor.fetchone()

        # Calculate haversine distance between user and event
        distance = calculate_haversine_distance(
            eval(home_location), event_dict["location"]
        )
        # Round the distance to 1 decimal
        distance = round(distance, 1)
        # Add extra attributes to the dictionary
        event_dict["distance_from_home_km"] = distance
        event_dict["participant_count"] = participant_count[0]

        formatted_created_events_result.append(event_dict)

    # Format the upcoming participated events into this array
    formatted_participating_future_result = []

    for event in participating_future_result:
        event_dict = format_event_tuple_to_dict(event_tuple=event)

        cursor.execute(GET_USERS_LOCATION_SQL, (username,))
        home_location = cursor.fetchone()[0]

        cursor.execute(GET_NUMER_OF_PARTICIPANTS_SQL, (event_dict["event_id"],))
        participant_count = cursor.fetchone()
        spaces_taken = participant_count[0]
        spaces_left = event_dict["max_participants"] - spaces_taken

        # Calculate haversine distance between user and event
        distance = calculate_haversine_distance(
            eval(home_location), event_dict["location"]
        )
        # Round the distance to 1 decimal
        distance = round(distance, 1)
        # Add extra attributes to the dictionary
        event_dict["distance_from_home_km"] = distance
        event_dict["spaces_left"] = spaces_left

        formatted_participating_future_result.append(event_dict)

    # Format the future created events into this array
    formatted_created_by_me_future_result = []

    for event in created_by_me_future_result:
        event_dict = format_event_tuple_to_dict(event_tuple=event)

        cursor.execute(GET_USERS_LOCATION_SQL, (username,))
        home_location = cursor.fetchone()[0]

        cursor.execute(GET_NUMER_OF_PARTICIPANTS_SQL, (event_dict["event_id"],))
        participant_count = cursor.fetchone()
        spaces_taken = participant_count[0]
        spaces_left = event_dict["max_participants"] - spaces_taken

        # Calculate haversine distance between user and event
        distance = calculate_haversine_distance(
            eval(home_location), event_dict["location"]
        )
        # Round the distance to 1 decimal
        distance = round(distance, 1)
        # Add extra attributes to the dictionary
        event_dict["distance_from_home_km"] = distance
        event_dict["spaces_left"] = spaces_left

        formatted_created_by_me_future_result.append(event_dict)

    final_list_of_events_formatted = [
        {
            "created_by_me": False,
            "upcoming": False,
            "events": formatted_participated_past_result,
        },
        {
            "created_by_me": False,
            "upcoming": True,
            "events": formatted_participating_future_result,
        },
        {
            "created_by_me": True,
            "upcoming": False,
            "events": formatted_created_events_result,
        },
        {
            "created_by_me": True,
            "upcoming": True,
            "events": formatted_created_by_me_future_result,
        },
    ]

    return final_list_of_events_formatted, 200
