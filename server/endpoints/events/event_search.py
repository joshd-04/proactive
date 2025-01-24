from ...util.format_conversion import format_event_tuple_to_dict
from ...util.haversine import calculate_haversine_distance


def event_search(db_pool, username, original_query, sort, quantity=10):
    try:
        quantity = int(quantity)
    except:
        return "Quantity must be an integer", 400
    conn = db_pool.getconn()
    cursor = conn.cursor()

    query = original_query.lower().replace(" ", "")
    if len(query) == 0:
        return "Query required", 400

    GET_USERS_LOCATION_SQL = """SELECT home_location FROM users WHERE username = %s;"""
    GET_FUTURE_EVENTS_SQL = f"SELECT * FROM events WHERE date_time > NOW();"
    SPACES_TAKEN = f"SELECT COUNT(*) FROM user_event_participation WHERE event_id = %s;"

    try:
        cursor.execute(GET_USERS_LOCATION_SQL, (username,))
        home_location = cursor.fetchone()[0]
        print(home_location, type(home_location))
        cursor.execute(GET_FUTURE_EVENTS_SQL)
        future_event_tuples = cursor.fetchall()

        # Convert tuples to dictionaries
        # Initialise a search_rank of zero
        future_events = []
        for event_tuple in future_event_tuples:
            event = format_event_tuple_to_dict(event_tuple)
            # Add some missing attributes (spaces_left, distance_from_home_km)
            cursor.execute(SPACES_TAKEN, (event["event_id"],))
            taken_spaces = cursor.fetchone()[0]

            spaces_left = event["max_participants"] - taken_spaces
            event["spaces_left"] = spaces_left

            # Calculate haversine distance between user and event

            distance = calculate_haversine_distance(
                eval(home_location), event["location"]
            )
            event["distance_from_home_km"] = round(distance, 1)

            search_rank = 0
            future_events.append(event)

            sport = event["sport"].lower().replace(" ", "")
            title = event["title"].lower().replace(" ", "")
            description = event["description"].lower().replace(" ", "")

            if query in sport or sport in query:
                search_rank += 10
            if query in title or title in query:
                search_rank += 5
            if query in description or description in query:
                search_rank += 2

            if search_rank > 0:
                pass

            event["search_rank"] = search_rank

        future_events.sort(key=lambda event: event["search_rank"], reverse=True)

    except Exception as error:
        print("error", error)
        return "There was an error", 500
    finally:
        db_pool.putconn(conn)

    print(future_events)

    return future_events[0:quantity]
