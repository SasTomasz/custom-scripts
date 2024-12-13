import folium
import geopandas as gpd
from shapely.geometry import Point, Polygon
from scipy.spatial import Delaunay
import numpy as np

# Points arranged to ensure a visible concave hull
points = [
    (50.058, 19.954),  # Point 1
    (50.058, 19.955),  # Point 2
    (50.059, 19.956),  # Point 3
    (50.060, 19.955),  # Point 4 - Outer point
    (50.060, 19.953),  # Point 5 - Outer point
    (50.059, 19.951),  # Point 6
    (50.058, 19.950),  # Point 7 - Creates indentation
    (50.057, 19.951),  # Point 8
    (50.057, 19.952),  # Point 9
    (50.056, 19.952),  # Additional Point for Concavity
    (50.056, 19.954),  # Additional Point for Concavity
]

# Function to create a convex hull
def convex_hull(points):
    gdf_points = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lat, lon in points])
    convex = gdf_points.geometry.unary_union.convex_hull
    print("Convex Hull:", convex)  # Debug output
    return convex

# Function to compute the alpha shape for concave hull
def alpha_shape(points, alpha):
    # Check for sufficient points
    if len(points) < 4:
        print("Not enough points to create a hull.")
        return gpd.GeoDataFrame(geometry=[])

    # Perform Delaunay triangulation
    tri = Delaunay(points)
    edges = set()

    # Create a set of edges
    for ia, ib, ic in tri.simplices:
        a = tuple(points[ia])  # Convert to tuple
        b = tuple(points[ib])  # Convert to tuple
        c = tuple(points[ic])  # Convert to tuple
        edges.add((a, b))
        edges.add((b, c))
        edges.add((c, a))

    # Filter edges based on alpha criterion
    alpha_edges = []
    for edge in edges:
        p1, p2 = edge
        distance = np.linalg.norm(np.array(p1) - np.array(p2))
        if distance < alpha:
            alpha_edges.append([p1, p2])

    # Collect unique points from valid edges to form a polygon
    unique_points = set()
    for edge in alpha_edges:
        unique_points.update(edge)

    # Ensure we have a valid polygon from unique points
    unique_points = [Point(p) for p in unique_points if isinstance(p, tuple)]

    if len(unique_points) < 3:
        print("Not enough unique points to create a polygon.")
        return gpd.GeoDataFrame(geometry=[])

    # Create polygon with unique points
    # Create a convex hull from unique points to ensure the polygon is valid
    polygon = Polygon([[p.x, p.y] for p in unique_points])

    if not polygon.is_valid:
        print("Created an invalid polygon from points.")
        return gpd.GeoDataFrame(geometry=[])

    return gpd.GeoDataFrame(geometry=[polygon])

# Function to add polygon to the Folium map
def add_polygon(map_obj, polygon, color, name):
    if polygon.is_empty or not polygon.is_valid:
        return
    if polygon.geom_type == 'Polygon':
        points = [(y, x) for x, y in polygon.exterior.coords]
        folium.Polygon(locations=points, color=color, fill=True, fill_opacity=0.5, popup=name).add_to(map_obj)

# Create a Folium map
m = folium.Map(location=[50.058, 19.954], zoom_start=14)  # Centered around the points

# Add points to the map
for lat, lon in points:
    folium.Marker([lat, lon], popup=f'Point: {lat}, {lon}').add_to(m)

# Create convex and concave hulls
convex = convex_hull(points)
concave = alpha_shape(np.array(points), alpha=0.005)  # Adjust alpha for concavity

# Create feature groups for convex and concave hulls
convex_group = folium.FeatureGroup(name='Convex Hull')
concave_group = folium.FeatureGroup(name='Concave Hull')

# Add hulls as polygons to their respective feature groups
add_polygon(convex_group, convex, 'blue', 'Convex Hull')
if not concave.empty:
    add_polygon(concave_group, concave.geometry.values[0], 'red', 'Concave Hull')
else:
    print("Concave hull is empty.")

# Add feature groups to the map
convex_group.add_to(m)
concave_group.add_to(m)

# Add layer control to toggle visibility
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save("mapa_obwiednie.html")

# Inform user
print("Map saved as 'mapa_obwiednie.html'. Open this file in your browser.")
