import json
from flask import request

from ...util.sql_statements import create_tables


def register_account(database_pool):
    data = request.get_json()
    data = json.loads(data)
    first_name = data["first_name"]
    last_name = data["last_name"]
    age = int(data["age"])
    home_location = data[
        "home_location"
    ]  # tuples not allowed in json, expecting a list/array
    username = data["username"]
    # assuming client-side has verified the strength of the unhashed password:
    password_hash = data["password_hash"]

    # Store the problems/errors, if any, in a dictionary
    issues = {}

    connection = database_pool.getconn()
    cursor = connection.cursor()
    getUserSQL = f"SELECT * FROM users WHERE username = '{username}';"
    # %s is a placeholder that will be filled later. psycopg2 prevents sql injections when we use %s
    insertUserSQL = f"INSERT INTO users (username, password_hash, first_name, last_name, age, home_location) VALUES (%s, %s, %s, %s, %s, POINT%s);"

    users_with_same_username = None

    try:
        create_tables(
            cursor=cursor
        )  # Make the tables just incase something fatal has happened
        # Check if username is taken
        cursor.execute(getUserSQL)
        users_with_same_username = cursor.fetchall()
        if len(users_with_same_username) > 0:
            issues["username"] = "Username is not unique."

        # Check if any of the data might violate database constraints

        ## Check if username is 3-15 characters
        if len(username) > 15:
            issues["username"] = "Username is too long. Max 15 chars."
        elif len(username) < 3:
            issues["username"] = "Username is too short. Min 3 chars."

        ## Check if first name is 2-25 characters
        if len(first_name) > 25:
            issues["first_name"] = "First name is too long. Max 25 chars."
        elif len(first_name) < 2:
            issues["first_name"] = "First name is too short. Min 2 chars."

        ## Check if last name is 2-25 characters
        if len(last_name) > 25:
            issues["last_name"] = "Last name is too long. Max 25 chars."
        elif len(last_name) < 2:
            issues["last_name"] = "Last name is too short. Min 2 chars."

        ## Check if age is under 16
        if age < 16:
            issues["age"] = "Minimum age to use the app is 16."

        ## Check if home location coordinates are valid points
        latitude = float(home_location[0])
        longitude = float(home_location[1])

        if latitude > 90 or latitude < -90:
            issues["home_location"] = "Latitude must be in region -90 to 90"
        if longitude > 180 or longitude < -180:
            issues["home_location"] = "Longitude must be in region -180 to 180"

        if len(issues.keys()) > 0:
            # If there are any problems with the data sent, send the list of problems to the user with error code 400 (bad request)
            print("issues found")
            print(issues)
            return (json.dumps(issues), 400)
        # Otherwise create a user record

        user_account_data = (
            username,
            password_hash,
            first_name,
            last_name,
            age,
            (latitude, longitude),
        )
        cursor.execute(insertUserSQL, user_account_data)
        connection.commit()  # Save changes to database (ACID compliance)

    except Exception as error:

        print(error)
        return (
            json.dumps(
                {
                    "message": "Error whilst creating your account. The account was not made."
                }
            ),
            500,
        )
    finally:

        database_pool.putconn(connection)

    return json.dumps({"message": "Account created. Proceed to log in."}), 201
