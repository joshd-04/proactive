from server.util.haversine import calculate_haversine_distance
from ...util.format_conversion import format_event_tuple_to_dict


def get_user_next_event(db_pool, username):
    # This SQL is extended from the one in events.py
    NEXT_EVENT_SQL = """SELECT events.* FROM user_event_participation INNER JOIN events ON user_event_participation.event_id = events.event_id WHERE user_event_participation.username = %s AND events.date_time > NOW() ORDER BY events.date_time ASC LIMIT 1;"""

    GET_USERS_LOCATION_SQL = """SELECT home_location FROM users WHERE username = %s;"""

    TAKEN_SPACES_SQL = (
        """SELECT COUNT(username) FROM user_event_participation WHERE event_id = %s;"""
    )

    conn = db_pool.getconn()
    cursor = conn.cursor()

    result_dict = {}
    try:
        cursor.execute(NEXT_EVENT_SQL, (username,))
        result = cursor.fetchone()
        if result:
            result_dict = format_event_tuple_to_dict(result)

            cursor.execute(GET_USERS_LOCATION_SQL, (username,))
            home_location = cursor.fetchone()[0]

            cursor.execute(TAKEN_SPACES_SQL, (result_dict["event_id"],))
            taken_spaces = cursor.fetchone()[0]

            # Calculate remaining spaces
            remaining_spaces = result_dict["max_participants"] - taken_spaces

            # Calculate haversine distance between user and event
            distance = calculate_haversine_distance(
                eval(home_location), result_dict["location"]
            )
            # Round the distance to 1 decimal
            distance = round(distance, 1)
            # Add extra attributes to the dictionary
            result_dict["distance_from_home_km"] = distance
            result_dict["spaces_left"] = remaining_spaces
    except Exception as error:
        print(error)
        return error, 500
    finally:
        db_pool.putconn(conn)
    return result_dict, 200
