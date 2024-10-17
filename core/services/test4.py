from shapely.geometry import Polygon
from scipy.spatial import Voronoi
import numpy as np
import matplotlib.pyplot as plt

# Example input: centers of zones (you would replace this with your actual data)
centers = np.array([[0, 0], [100, 100], [200, 200], [300, 100], [100, 300]])

# Compute the Voronoi diagram based on the centers
vor = Voronoi(centers)

# Function to check if a region forms a valid polygon
def is_valid_polygon(region, vertices):
    # Ensure the region has enough vertices and is not a region that extends to infinity
    if len(region) < 3 or -1 in region:
        return False
    # Get the actual polygon points and check for validity
    polygon_points = vertices[region]
    if len(polygon_points) >= 3:
        # Ensure that the polygon is closed (first point == last point)
        if not np.array_equal(polygon_points[0], polygon_points[-1]):
            polygon_points = np.vstack([polygon_points, polygon_points[0]])
        return True
    return False

# Create sub-zone polygons, filtering invalid ones
sub_zone_polygons = []

for region in vor.regions:
    if is_valid_polygon(region, vor.vertices):
        sub_zone_polygons.append(Polygon(vor.vertices[region]))

# Plot the Voronoi diagram for visualization (optional)
fig, ax = plt.subplots()

# Plot the Voronoi vertices and regions
ax.plot(vor.vertices[:, 0], vor.vertices[:, 1], 'o')  # Voronoi vertices

# Plot the sub-zone polygons
for polygon in sub_zone_polygons:
    if polygon.is_valid:
        x, y = polygon.exterior.xy
        ax.fill(x, y, alpha=0.4)  # Fill the polygons with some transparency

# Plot the centers of the zones
ax.plot(centers[:, 0], centers[:, 1], 'ro')  # Zone centers as red points

plt.show()
