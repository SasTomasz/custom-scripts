# Importing points from points.py
from points import points  # Replace local 'points' with those from points.py

import folium

# Create a map at the center of the first point
m = folium.Map(location=points[0], zoom_start=13)

# Add points from points.py to the map
for point in points:
    folium.Marker(location=point).add_to(m)

# Save the map to an HTML file
m.save('updated_map_with_points.html')
