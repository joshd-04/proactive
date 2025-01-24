from flask import request


def create_review(db_pool):
    # Expecting rating, title and review
    # to be in the request body JSON
    data = request.get_json()

    try:
        username = data["username"]
        event_id = data["event_id"]
        rating = data["rating"]
        title = data["title"]
        review = data["review"]
    except:
        return (
            "'username', 'event_id', 'rating', 'title' and 'review' are required values in the JSON body",
            422,  # Error code 442: unprocessable content
        )

    if rating > 5.0 or rating < 1.0:
        return "Rating must be between 5.0 and 1.0", 400
    if len(review) <= 60:
        return "Review must have atleast 60 characters", 400

    INSERT_REVIEW_SQL = "INSERT INTO event_ratings (username, event_id, rating, title, review) VALUES (%s, %s, %s, %s, %s);"

    conn = db_pool.getconn()
    cursor = conn.cursor()

    try:
        data_tuple = (username, event_id, rating, title, review)
        cursor.execute(INSERT_REVIEW_SQL, data_tuple)

    except Exception as error:
        print(error)
        return (
            "There was an unexpected error whilst creating the review. The review was not created.",
            500,
        )
    else:
        # If there is no error, save the changes
        conn.commit()
    finally:
        db_pool.putconn(conn)

    # Return nothing, with a 201 (created) status code
    return "", 201
