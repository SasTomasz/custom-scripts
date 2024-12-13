# This script generate points with its latitude and longitude that are in the border of circle with specific radius and
# starting point

import math

# Constants
center_lat = 50.05083000359872
center_lon = 19.944953484012327
radius = 752  # in meters
earth_radius = 6371000  # in meters


# Function to generate border points
def generate_border_points(l_center_lat, l_center_lon, l_radius, segments=360):
    l_border_points = []
    for angle in range(segments):
        bearing = math.radians(angle)
        latitude = math.asin(
            math.sin(math.radians(l_center_lat)) * math.cos(l_radius / earth_radius) +
            math.cos(math.radians(l_center_lat)) * math.sin(l_radius / earth_radius) * math.cos(bearing)
        )
        longitude = math.radians(l_center_lon) + math.atan2(
            math.sin(bearing) * math.sin(l_radius / earth_radius) * math.cos(math.radians(l_center_lat)),
            math.cos(l_radius / earth_radius) - math.sin(math.radians(l_center_lat)) * math.sin(latitude)
        )

        latitude = math.degrees(latitude)
        longitude = math.degrees(longitude)

        # Debug: Check distance from the center
        calculated_distance = (
                math.acos(
                    math.sin(math.radians(l_center_lat)) * math.sin(math.radians(latitude)) +
                    math.cos(math.radians(l_center_lat)) * math.cos(math.radians(latitude)) *
                    math.cos(math.radians(longitude - l_center_lon))
                ) * earth_radius
        )
        if abs(calculated_distance - l_radius) > 0.1:  # Allow slight deviation
            print(f"Point off-radius: Latitude: {latitude}, Longitude: {longitude}, Distance: {calculated_distance}")

        l_border_points.append((latitude, longitude))
    return l_border_points


# Generate and print border points
border_points = generate_border_points(center_lat, center_lon, radius)
for lat, lon in border_points:
    print(f"Latitude: {lat}, Longitude: {lon}")

# Test points
test_points = [
    (50.05293853754094, 19.939975658188146),  # Inside circle
    (50.04995276492667, 19.950849627013234),  # Inside circle
    (50.057184993640725, 19.94135073381801),  # On the border
    (50.05759187190787, 19.944769643396256),  # On the border
    (50.069428161962975, 19.94312396770417),  # Outside circle
    (50.08311851004129, 20.011916103654706),  # Outside circle
]

# Debug: Check test points distance from center
print("\nTesting specific points:")
for lat, lon in test_points:
    distance = (
            math.acos(
                math.sin(math.radians(center_lat)) * math.sin(math.radians(lat)) +
                math.cos(math.radians(center_lat)) * math.cos(math.radians(lat)) *
                math.cos(math.radians(lon - center_lon))
            ) * earth_radius
    )
    print(
        f"Point Latitude: {lat}, Longitude: {lon}, Distance: {distance}, {'Inside' if distance <= radius else 'Outside'}")
