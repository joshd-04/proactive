class SummaryWeights:
    def __init__(self):
        self.weights_dict = {}

    def add_value(self, attribute_name, weight):
        # Get a list of all the dictionary keys
        keys = self.weights_dict.keys()

        # If the parameter attribute name is present, add to it, otherwise initalise it
        if attribute_name in keys:
            self.weights_dict[attribute_name] += weight
        else:
            self.weights_dict[attribute_name] = weight

    def get_top_values(self, quantity):
        # Extract the items from the dict, and sort them based on the second item (the weight) for each key-value pair
        items = self.weights_dict.items()
        sorted_items = sorted(items, key=lambda item: item[1], reverse=True)

        top_values = []
        for i in range(quantity):
            if i <= len(sorted_items) - 1:
                top_values.append(sorted_items[i][0])

        return top_values
