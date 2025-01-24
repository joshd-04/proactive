def get_reviews(db_pool, username, event_id):
    try:
        if event_id != None:
            event_id = int(event_id)
    except:
        return (
            "The event id parameter must be an integer, either fix this or remove the parameter completely",
            400,
        )
    if type(username) == "str":
        if len(username) == 0:
            return (
                "Username parameter is missing its value, fix this or remove the parameter completely",
                400,
            )

    conn = db_pool.getconn()
    cursor = conn.cursor()

    GET_REVIEWS_USERNAME_SQL = "SELECT * FROM event_ratings WHERE username = %s;"
    GET_REVIEWS_EVENT_ID_SQL = "SELECT * FROM event_ratings WHERE event_id = %s;"
    GET_REVIEWS_USERNAME_EVENT_ID_SQL = (
        "SELECT * FROM event_ratings WHERE username = %s AND event_id = %s;"
    )

    try:
        # Username only
        if username != None and event_id == None:
            cursor.execute(GET_REVIEWS_USERNAME_SQL, (username,))
        # Event id only
        elif username == None and event_id != None:
            cursor.execute(GET_REVIEWS_EVENT_ID_SQL, (event_id,))
        # Both username and event id
        elif username != None and event_id != None:
            cursor.execute(
                GET_REVIEWS_USERNAME_EVENT_ID_SQL,
                (
                    username,
                    event_id,
                ),
            )
        else:
            raise Exception("Cannot query database without both username and event_id")

        result_tuples = cursor.fetchall()
        result = []

        for rating_tuple in result_tuples:
            rating = {
                "username": rating_tuple[0],
                "event_id": rating_tuple[1],
                "rating": rating_tuple[2],
                "title": rating_tuple[3],
                "review": rating_tuple[4],
            }
            result.append(rating)

    except Exception as error:
        print(error)
        return "There was an unexpected error trying to fetch the reviews", 500

    finally:
        db_pool.putconn(conn)

    return result, 200
