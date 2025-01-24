# GET USER
import json


def get_user(db_pool, username):
    GET_USER_SQL = """SELECT * FROM users WHERE username = %s;"""

    conn = db_pool.getconn()
    cursor = conn.cursor()
    try:
        cursor.execute(GET_USER_SQL, (username,))
        # There should be only one result or none. So fetch the only one result.
        user = cursor.fetchone()
    except Exception as error:
        print("There was an error")
        print(error)
    finally:
        db_pool.putconn(conn)

    if user:
        user_dict = {
            "username": user[0],
            "password_hash": user[1],
            "access_level": user[2],
            "first_name": user[3],
            "last_name": user[4],
            "age": user[5],
            "home_location": user[6],
        }
        return json.dumps(user_dict), 200
    else:
        return f"User {username} does not exist", 404
