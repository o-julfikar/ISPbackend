from shapely.geometry import MultiPolygon, Polygon
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

# Example MultiPolygon
multipolygon = MultiPolygon([
    Polygon([(0, 0), (2, 0), (2, 2), (0, 2)]),
    Polygon([(3, 1), (5, 1), (5, 3), (3, 3)])
])

# Example Polygon
polygon = Polygon([(1, 1), (4, 1), (4, 2), (1, 2)])

# Extract points from MultiPolygon
print([p for poly in multipolygon.geoms for p in poly.exterior.coords])
points = np.array([p for poly in multipolygon.geoms for p in poly.exterior.coords])

# Extract points from the Polygon
polygon_points = np.array(polygon.exterior.coords)


# Create Voronoi diagram
vor = Voronoi(points)
#
# # Plotting
fig, ax = plt.subplots()
#
# # Plot Voronoi diagram
voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='orange', line_width=2, point_size=5)

# Plot the MultiPolygon
for poly in multipolygon.geoms:
    x, y = poly.exterior.xy
    ax.fill(x, y, alpha=0.5, fc='blue', ec='black', label='MultiPolygon')

# Plot the Polygon
x, y = polygon.exterior.xy
ax.fill(x, y, alpha=0.5, fc='green', ec='black', label='Polygon')

# Adding legend
plt.legend()
plt.title('Voronoi Diagram with MultiPolygon and Polygon')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.axis('equal')
plt.grid()

plt.show()
