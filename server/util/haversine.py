import math


def calculate_haversine_distance(point1, point2):
    radius = 6371  # km, of the earth

    radians_conversion = math.pi / 180
    # latitude = point[0]
    # longitude = point[1]

    value = (
        0.5
        - math.cos((point2[0] - point1[0]) * radians_conversion) / 2
        + math.cos(point1[0] * radians_conversion)
        * math.cos(point2[0] * radians_conversion)
        * (1 - math.cos((point2[1] - point1[1]) * radians_conversion))
        / 2
    )

    return 2 * radius * math.asin(math.sqrt(value))
