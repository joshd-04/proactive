def calculate_event_field_weight(event_attribute, top_user_attributes, weight_tuple):
    # Loop over each of the user's favoured attributes
    for i in range(len(top_user_attributes)):
        # If the users i-th attribute matches the event's attribute
        if top_user_attributes[i] == event_attribute:
            # ... check if index i corresponds to a weight value
            if i > len(weight_tuple) - 1:
                # ... if not, return 0
                return 0
            return weight_tuple[i]
    return 0
