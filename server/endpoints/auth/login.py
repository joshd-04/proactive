import json
from flask import request
from ...util.sql_statements import create_tables


def login(database_pool):
    # Parse the JSON send in the request. JSON is a standard in HTTP payloads.
    data = request.get_json()
    data = json.loads(data)
    username = data["username"]
    password_hash = data["password_hash"]

    # Again the use of %s is to prevent sql injection, and the username can replace it during cursor.execute()
    get_username_password_hash = f"SELECT * FROM users WHERE username = %s;"

    connection = database_pool.getconn()
    cursor = connection.cursor()

    issues = {}
    login_successful = False  # Log in flag
    user_account = None
    try:
        create_tables(cursor=cursor)  # Just incase they dont exist already
        cursor.execute(get_username_password_hash, (username,))
        results = cursor.fetchall()
        if len(results) == 0:
            issues["username"] = f"Account does not exist with username: '{username}'"
        if len(results) > 1:
            issues["username"] = f"Multiple accounts found with username: {username}"

        if len(results) == 1:
            user_account = results[0]  # Stores user account
            actual_password_hash = user_account[1]

            if password_hash == actual_password_hash:
                login_successful = True
            else:
                issues["password"] = "Invalid password"

        connection.commit()
    except Exception as error:
        print(error)
    finally:
        database_pool.putconn(connection)

    if login_successful and user_account:
        user_account_dictionary = {
            "username": user_account[0],
            "password_hash": user_account[1],
            "access_level": user_account[2],
            "first_name": user_account[3],
            "last_name": user_account[4],
            "age": user_account[5],
            "home_location": user_account[6],
        }
        return (json.dumps(user_account_dictionary), 200)
    else:
        return (json.dumps(issues), 401)
