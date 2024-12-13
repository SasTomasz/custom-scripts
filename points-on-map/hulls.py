import folium
import geopandas as gpd
from shapely.geometry import Point, Polygon
from scipy.spatial import Delaunay
import numpy as np

# Sample list of geographical points
points = [
    (50.058981119057506, 19.954675472158453),
    (50.05770909025181, 19.94406863517483),
    (50.055585081880366, 19.951772170794726),
    (50.049398100539534, 19.935561188845963),
    (50.06902231874633, 19.95324933928131),
    (50.054273123671436, 19.942282152494847),
    (50.06637451782462, 19.951435701622973),
]

# Function to create a convex hull
def convex_hull(points):
    gdf_points = gpd.GeoDataFrame(geometry=[Point(lon, lat) for lat, lon in points])
    return gdf_points.geometry.unary_union.convex_hull

# Function to compute the alpha shape for concave hull
def alpha_shape(points, alpha):
    if len(points) < 4:
        return None  # Not enough points to form a hull

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

    # Create a polygon if there are enough unique points
    if len(unique_points) >= 3:
        return gpd.GeoDataFrame(geometry=[Polygon(unique_points)])
    else:
        return gpd.GeoDataFrame(geometry=[])

# Function to add polygon to the Folium map
def add_polygon(map_obj, polygon, color, name):
    if polygon.is_empty:
        return
    if polygon.geom_type == 'Polygon':
        points = [(y, x) for x, y in polygon.exterior.coords]
        folium.Polygon(locations=points, color=color, fill=True, fill_opacity=0.2, popup=name).add_to(map_obj)
    elif polygon.geom_type == 'GeometryCollection':
        for geom in polygon.geoms:
            if geom.geom_type == 'Polygon':
                points = [(y, x) for x, y in geom.exterior.coords]
                folium.Polygon(locations=points, color=color, fill=True, fill_opacity=0.2, popup=name).add_to(map_obj)

# Create a Folium map
m = folium.Map(location=[50.058, 19.95], zoom_start=13)  # Centered around the points

# Add points to the map
for lat, lon in points:
    folium.Marker([lat, lon], popup=f'Point: {lat}, {lon}').add_to(m)

# Create convex and concave hulls
convex = convex_hull(points)
concave = alpha_shape(np.array(points), alpha=1.99)  # Adjust alpha as needed

# Create feature groups for convex and concave hulls
convex_group = folium.FeatureGroup(name='Convex Hull')
concave_group = folium.FeatureGroup(name='Concave Hull')

# Add hulls as polygons to their respective feature groups
add_polygon(convex_group, convex, 'blue', 'Convex Hull')
if not concave.empty:
    add_polygon(concave_group, concave.geometry.values[0], 'red', 'Concave Hull')

# Add feature groups to the map
convex_group.add_to(m)
concave_group.add_to(m)

# Add layer control to toggle visibility
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save("mapa_obwiednie.html")

# Inform user
print("Map saved as 'mapa_obwiednie.html'. Open this file in your browser.")
