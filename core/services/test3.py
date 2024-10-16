from shapely.geometry import MultiPolygon, Polygon
from descartes import PolygonPatch
import matplotlib.pyplot as plt

if __name__ == "__main__":

    # Create a MultiPolygon object
    polygons = MultiPolygon([
        Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
        Polygon([(2, 2), (3, 2), (3, 3), (2, 3)]),
        Polygon([(4, 4), (5, 4), (5, 5), (4, 5)])
    ])

    # Initialize plot
    fig, ax = plt.subplots()

    # Check and plot each Polygon in the MultiPolygon
    if isinstance(polygons, MultiPolygon):
        for p in polygons.geoms:
            print(p)  # Debugging line to check the polygon
            if p.is_valid:  # Ensure the polygon is valid
                patch = PolygonPatch(p, facecolor="lightcoral", edgecolor="black", alpha=0.5)
                ax.add_patch(patch)
            else:
                print("Invalid polygon:", p)
    else:
        if polygons.is_valid:
            patch = PolygonPatch(polygons, facecolor="lightyellow", edgecolor="black", alpha=0.5)
            ax.add_patch(patch)

    # Set plot limits and show
    ax.set_xlim(-1, 6)
    ax.set_ylim(-1, 6)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
