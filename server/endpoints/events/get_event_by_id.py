from ...util.format_conversion import format_event_tuple_to_dict


def get_event_by_id(db_pool, event_id):
    try:
        event_id = int(event_id)
    except:
        return "Event id must be an integer", 400

    conn = db_pool.getconn()
    cursor = conn.cursor()

    GET_EVENT_SQL = "SELECT * FROM events WHERE event_id = %s;"
    SPACES_TAKEN = f"SELECT COUNT(*) FROM user_event_participation WHERE event_id = %s;"

    try:
        cursor.execute(GET_EVENT_SQL, (event_id,))
        event_tuple = cursor.fetchone()
        if event_tuple == None:
            return "Event not found", 404
        event = format_event_tuple_to_dict(event_tuple)

        cursor.execute(SPACES_TAKEN, (event_id,))
        taken_spaces = cursor.fetchone()[0]
        event["spaces_left"] = round(event["max_participants"] - taken_spaces, 1)

    except Exception as error:
        print(error)
        return "There was an unexpected error when fetching the event", 500
    finally:
        db_pool.putconn(conn)

    return event, 200
