def delete_event(db_pool, event_id, username):
    conn = db_pool.getconn()
    cursor = conn.cursor()

    GET_EVENT_SQL = "SELECT event_creator FROM events WHERE event_id = %s"
    DELETE_EVENT_SQL = "DELETE FROM events WHERE event_id = %s;"

    # 1. Ensure the username of the account matches the event creator
    # 2. Delete the event if so

    try:
        cursor.execute(GET_EVENT_SQL, (event_id,))
        event_creator = cursor.fetchone()[0]

        if event_creator == username:
            cursor.execute(DELETE_EVENT_SQL, (event_id,))
        else:
            return "You are not permitted to perform this action", 403
    except Exception as error:
        print(error)
        return (
            "There was an error trying to delete the event, it has not been deleted.",
            500,
        )
    else:
        # Save the changes to the database if there was no error
        # Only save the changes if there was no error
        conn.commit()
    finally:
        db_pool.putconn(conn)

    return "", 200
