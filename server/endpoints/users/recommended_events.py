from ...util.format_conversion import format_user_tuple_to_dict
from ...util.format_conversion import format_event_tuple_to_dict
from ...util.haversine import calculate_haversine_distance

from ...util.recommendation_util.summary_weights_class import SummaryWeights
from ...util.recommendation_util.calculate_event_field_weight import (
    calculate_event_field_weight,
)


# GET /RECOMMENDED EVENTS
def recommended_events(db_pool, username, event_quantity):
    conn = db_pool.getconn()
    cursor = conn.cursor()
    weekdays = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    try:
        # 1. Get the user from their username
        GET_USER_SQL = "SELECT * FROM users WHERE username = %s;"
        cursor.execute(GET_USER_SQL, (username,))
        users_result = cursor.fetchall()
        if len(users_result) != 1:
            return "Provided username does not correspond to a unique account", 400
        user_tuple = users_result[0]

        user_dict = format_user_tuple_to_dict(user_tuple)

        # 2. Find the events they have participated in and attended
        GET_PARTICIPATED_EVENTS_SQL = "SELECT events.* FROM user_event_participation INNER JOIN events ON user_event_participation.event_id = events.event_id WHERE user_event_participation.username = %s AND user_event_participation.did_attend = True;"
        events_list = []
        cursor.execute(GET_PARTICIPATED_EVENTS_SQL, (username,))
        events_result = cursor.fetchall()

        for event_tuple in events_result:
            event_dict = format_event_tuple_to_dict(event_tuple)
            events_list.append(event_dict)

        # 3. Get the rating, for each event (if it exists)
        GET_RATING_OF_EVENT = "SELECT * FROM event_ratings WHERE event_id = %s;"
        for event in events_list:
            cursor.execute(GET_RATING_OF_EVENT, (event["event_id"],))
            ratings_result = cursor.fetchone()
            if ratings_result:
                rating_dict = {
                    "username": ratings_result[0],
                    "event_id": ratings_result[1],
                    "rating": ratings_result[2],
                    "title": ratings_result[3],
                    "review": ratings_result[4],
                }
                event["rating"] = rating_dict

        # 4. Create summary dictionaries containing the users summarised history based on weightings
        ## 5 stars = 40 weight
        ## 4 stars = 25 weight
        ## 3 stars = 10 weight
        ## 2 stars = -10 weight
        ## 1 star = -30 weight

        # Each attribute gets its own weight class
        summary_weights = {
            "sport": SummaryWeights(),
            "intensity": SummaryWeights(),
            "skill_level": SummaryWeights(),
            "max_participants": SummaryWeights(),
            "event_creator": SummaryWeights(),
            "time": SummaryWeights(),
            "day": SummaryWeights(),
        }

        for event in events_list:
            # Extract the rating score from the event dictionary
            rating = event["rating"]["rating"]

            if rating >= 1.0 and rating < 2.0:
                weight = -30
            elif rating >= 2.0 and rating < 3.0:
                weight = -10
            elif rating >= 3.0 and rating < 3.5:
                weight = 10
            elif rating >= 3.5 and rating < 4.0:
                weight = 20
            elif rating >= 4.0 and rating < 4.5:
                weight = 35
            elif rating >= 4.5 and rating <= 5.0:
                weight = 50
            else:
                # If there is an unexpected condition, do not contribute to the recommendation process (by having a weight of 0)
                weight = 0

            # Add this event's weights to the summary weights
            # Convert to lowercase normalise each attribute before it is used as a dictionary key
            sport = event["sport"].lower()
            summary_weights["sport"].add_value(attribute_name=sport, weight=weight)

            intensity = event["intensity"].lower()
            summary_weights["intensity"].add_value(
                attribute_name=intensity, weight=weight
            )

            skill_level = event["skill_level"].lower()
            summary_weights["skill_level"].add_value(
                attribute_name=skill_level, weight=weight
            )

            # Round max_participants to the nearest 5 above the actual value
            # So an event with 2 m_p will be rounded to 5
            # An event with 31 will be rounded to 35
            # This is done to improve the 'groupability' of this attribute
            # Use (x DIV 5) + 1
            max_participants_precision = 5

            max_participants = (
                event["max_participants"] // max_participants_precision
            ) + 1
            summary_weights["max_participants"].add_value(
                attribute_name=max_participants, weight=weight
            )

            event_creator = event["event_creator"].lower()
            summary_weights["event_creator"].add_value(
                attribute_name=event_creator, weight=weight
            )

            date_time = event["date_time"]
            hour = date_time.hour
            summary_weights["time"].add_value(attribute_name=hour, weight=weight)

            day = weekdays[date_time.weekday()]
            summary_weights["day"].add_value(attribute_name=day, weight=weight)

        # 5. Get top 3 data points for all summarised variables
        quantity = 3
        top_sports = summary_weights["sport"].get_top_values(quantity)
        top_intensities = summary_weights["intensity"].get_top_values(quantity)
        top_skill_levels = summary_weights["skill_level"].get_top_values(quantity)
        top_max_participants = summary_weights["max_participants"].get_top_values(
            quantity
        )
        top_event_creators = summary_weights["event_creator"].get_top_values(quantity)
        top_times = summary_weights["time"].get_top_values(quantity)
        top_days = summary_weights["day"].get_top_values(quantity)

        # 6. Using a new weighting system, rank events
        event_pool = []  # An array containing events that will be sent to the user

        GET_ALL_UPCOMING_EVENTS_SQL = f"SELECT * FROM events WHERE date_time > NOW();"

        cursor.execute(GET_ALL_UPCOMING_EVENTS_SQL)
        upcoming_event_tuples = cursor.fetchall()
        upcoming_events = []

        # Convert tuples to dictionaries
        for event_tuple in upcoming_event_tuples:
            event_dict = format_event_tuple_to_dict(event_tuple)
            upcoming_events.append(event_dict)

        # Filter far events out
        for event in upcoming_events:
            haversine_distance = calculate_haversine_distance(
                event["location"], user_dict["home_location"]
            )

            # Filter out events that are too far from the user.
            max_distance = 1000
            if haversine_distance <= max_distance:
                # Add the distance to the event dictionary
                event["distance_from_home_km"] = round(haversine_distance, 1)

                # Add the spaces left to the event. If the event is full: don't add it to the event pool
                GET_PARTICIPANT_COUNT_SQL = """SELECT COUNT(username) FROM user_event_participation WHERE event_id = %s;"""
                cursor.execute(GET_PARTICIPANT_COUNT_SQL, (event["event_id"],))
                participant_count = cursor.fetchone()[0]

                if participant_count >= event["max_participants"]:
                    # Go to next iteration in the for loop
                    continue
                else:
                    event["spaces_left"] = event["max_participants"] - participant_count
                    event_pool.append(event)

        # Add weightings to remaining events
        for event in event_pool:
            event["weight"] = 0

            # Sport, intensity, skill level, max participants, event creator, time, day
            event_sport = event["sport"]
            event_intensity = event["intensity"]
            event_skill_level = event["skill_level"]
            event_max_participants = (event["max_participants"] // 5) + 1
            event_event_creator = event["event_creator"]
            event_date_time = event["date_time"]
            event_time = event_date_time.hour
            event_day = weekdays[event_date_time.weekday()]

            event["weight"] += calculate_event_field_weight(
                event_sport, top_sports, (20, 15, 10)
            )
            event["weight"] += calculate_event_field_weight(
                event_intensity, top_intensities, (10, 5, 0)
            )
            event["weight"] += calculate_event_field_weight(
                event_skill_level, top_skill_levels, (15, 10, 5)
            )

            event["weight"] += calculate_event_field_weight(
                event_max_participants, top_max_participants, (5, 5, 5)
            )

            event["weight"] += calculate_event_field_weight(
                event_event_creator, top_event_creators, (25, 20, 15)
            )

            event["weight"] += calculate_event_field_weight(
                event_time, top_times, (20, 15, 10)
            )

            event["weight"] += calculate_event_field_weight(
                event_day, top_days, (15, 10, 5)
            )

        # Sort the event_pool by the event weights
        event_pool.sort(key=lambda x: x["weight"], reverse=True)

    except Exception as error:
        print(error)
        return "There was an unexpected error!", 400

    finally:
        db_pool.putconn(conn)

    try:
        event_quantity = int(event_quantity)
    except:
        # Default event quantity to return
        event_quantity = 10

    return event_pool[:event_quantity], 200
