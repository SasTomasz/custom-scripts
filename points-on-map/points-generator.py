import numpy as np

# Geographic coordinates of Krakow
krakow_center_lat = 50.0646501
krakow_center_lon = 19.9449799

# Number of points
num_points = 300

# Generating random points around Krakow
# Normal distribution: mean (lat/lon) and small standard deviation to keep the points relatively close to each other
latitudes = np.random.normal(loc=krakow_center_lat, scale=0.01, size=num_points)
longitudes = np.random.normal(loc=krakow_center_lon, scale=0.01, size=num_points)

# Creating a list of points as tuples (lat, lon)
points = list(zip(latitudes, longitudes))

# Saving to a file
with open('./points.py', 'w') as f:
    f.write("points = [\n")
    for point in points:
        f.write(f"    ({point[0]}, {point[1]}),\n")
    f.write("]\n")

print("Points have been saved to the file 'points.py'.")
