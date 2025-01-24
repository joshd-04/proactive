def format_event_tuple_to_dict(event_tuple):
    event_dict = {
        "event_id": event_tuple[0],
        "title": event_tuple[1],
        "description": event_tuple[2],
        "sport": event_tuple[3],
        "intensity": event_tuple[4],
        "skill_level": event_tuple[5],
        "max_participants": event_tuple[6],
        "location": eval(event_tuple[7]),
        "event_creator": event_tuple[8],
        "date_time": event_tuple[9],
    }
    return event_dict


def format_user_tuple_to_dict(user_tuple):
    user_dict = {
        "username": user_tuple[0],
        "password_hash": user_tuple[1],
        "access_level": user_tuple[2],
        "first_name": user_tuple[3],
        "last_name": user_tuple[4],
        "age": user_tuple[5],
        "home_location": eval(user_tuple[6]),
    }

    return user_dict
