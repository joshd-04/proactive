def get_reviews_by_event_id(db_pool, event_id):
    try:
        event_id = int(event_id)
    except:
        return "Event id must be an integer", 400
    conn = db_pool.getconn()
    cursor = conn.cursor()

    GET_REVIEWS_SQL = "SELECT * FROM event_ratings WHERE event_id = %s;"

    try:
        cursor.execute(GET_REVIEWS_SQL, (event_id,))
        results = cursor.fetchall()
        formatted_result = []

        for result_tuple in results:
            result = {
                "username": result_tuple[0],
                "event_id": result_tuple[1],
                "rating": result_tuple[2],
                "title": result_tuple[3],
                "review": result_tuple[4],
            }
            formatted_result.append(result)

    except Exception as error:
        print(error)
        return "There was an error whilst fetching the reviews of the event", 500
    finally:
        db_pool.putconn(conn)

    return formatted_result, 200
