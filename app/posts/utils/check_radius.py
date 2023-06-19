import math


def haversine_distance(latitude1, longitude1, distance_km):
    # Earth's radius in kilometers
    radius_km = 6371.0

    # Convert distance from kilometers to radians
    distance_rad = distance_km / radius_km

    # Convert latitude and longitude to radians
    lat1_rad = math.radians(latitude1)
    lon1_rad = math.radians(longitude1)

    # Calculate minimum and maximum latitude
    min_latitude = math.degrees(lat1_rad - distance_rad)
    max_latitude = math.degrees(lat1_rad + distance_rad)

    # Calculate the difference in longitude for the given latitude
    delta_longitude = math.asin(math.sin(distance_rad) / math.cos(lat1_rad))

    # Calculate minimum and maximum longitude
    min_longitude = math.degrees(lon1_rad - delta_longitude)
    max_longitude = math.degrees(lon1_rad + delta_longitude)

    return min_latitude, max_latitude, min_longitude, max_longitude


# # Example usage
# latitude1 = 43.218422
# longitude1 = 76.9279
# distance_km = 2

# min_lat, max_lat, min_lon, max_lon = calculate_coordinate_range(
#     latitude1, longitude1, distance_km
# )

# print(f"Latitude range: {min_lat} to {max_lat}")
# print(f"Longitude range: {min_lon} to {max_lon}")


######## WHY JUST A FUNCTION !!! #########
