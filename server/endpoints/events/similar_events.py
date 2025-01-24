from ...util.format_conversion import format_event_tuple_to_dict
from ...util.haversine import calculate_haversine_distance


def get_similar_events(db_pool, event_id, quantity=5):
    try:
        quantity = int(quantity)
    except:
        return "Quantity must be an integer", 404

    conn = db_pool.getconn()
    cursor = conn.cursor()

    GET_EVENTS_SQL = f"SELECT * FROM events WHERE date_time > NOW() AND event_id <> %s;"

    GET_COMPARISON_EVENT_SQL = f"SELECT * FROM events WHERE event_id = %s;"

    try:
        cursor.execute(GET_COMPARISON_EVENT_SQL, (event_id,))
        comparison_event = format_event_tuple_to_dict(cursor.fetchone())

        cursor.execute(GET_EVENTS_SQL, (event_id,))
        result_tuples = cursor.fetchall()
        result = []

        for event_tuple in result_tuples:
            event = format_event_tuple_to_dict(event_tuple)

            # If event is beyond 20km away, ignore this event
            if (
                calculate_haversine_distance(
                    event["location"], comparison_event["location"]
                )
                > 20
            ):
                continue

            weight = 0

            if event["sport"].lower() == comparison_event["sport"].lower():
                weight += 30
            if event["intensity"].lower() == comparison_event["intensity"].lower():
                weight += 10
            if event["skill_level"].lower() == comparison_event["skill_level"].lower():
                weight += 10

            # Round max_participants to the nearest 5 above the actual value
            # So an event with 2 m_p will be rounded to 5
            # An event with 31 will be rounded to 35
            # This is done to improve the 'groupability' of this attribute
            # Use (x DIV 5) + 1
            max_participants_precision = 5

            max_participants = (
                event["max_participants"] // max_participants_precision
            ) + 1

            comparison_max_participants = (
                comparison_event["max_participants"] // max_participants_precision
            ) + 1

            if max_participants == comparison_max_participants:
                weight += 20

            # If event is within 5 km then class add the weight for similarity
            if (
                calculate_haversine_distance(
                    event["location"], comparison_event["location"]
                )
                < 5
            ):
                weight += 15

            if (
                event["event_creator"].lower()
                == comparison_event["event_creator"].lower()
            ):
                weight += 20

            date_time = event["date_time"]
            date_time_comparison = comparison_event["date_time"]

            if date_time.hour == date_time_comparison.hour:
                weight += 15

            if date_time.weekday() == date_time.weekday():
                weight += 10

            event["weight"] = weight

            result.append(event)
        sorted_result = sorted(result, key=lambda x: x["weight"], reverse=True)

    except Exception as error:
        print(error)
        return (
            "There was an unexpected error whilst trying to find similar events to this event",
            500,
        )
    finally:
        db_pool.putconn(conn)

    return sorted_result[:quantity], 200
