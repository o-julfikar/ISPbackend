import os
import random
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point, MultiPolygon
from multiprocessing import Pool
from descartes import PolygonPatch


# Function to allocate zones (ML/AI can be integrated here)
def zone_allocation(area, population_density):
    """Assign land use zoning and public services based on area and population."""
    residential = area * 0.3  # 30% residential
    agriculture = area * 0.35  # 35% agricultural
    industrial = area * 0.2  # 20% industrial
    green_space = area * 0.15  # 15% green space

    total_public_services = area * 0.1  # 10% for public services
    healthcare = total_public_services * 0.3
    education = total_public_services * 0.3
    admin = total_public_services * 0.4

    return {
        "land_use": {
            "residential": residential,
            "agriculture": agriculture,
            "industrial": industrial,
            "green_space": green_space
        },
        "public_services": {
            "total_public_services": total_public_services,
            "healthcare": healthcare,
            "education": education,
            "admin": admin
        }
    }


# Function to generate spatial planning for each division
def generate_spatial_plan(division_data):
    name, geometry, population_density = division_data
    area = geometry.area

    # Example connection data for the divisions
    divisions_connection_data = {
        "divisions": [
            {
                "name": "Barishal",
                "connected_to": ["Dhaka", "Khulna"]
            },
            {
                "name": "Chittagong",
                "connected_to": ["Dhaka", "Sylhet"]
            },
        ]
    }

    allocations = zone_allocation(area, population_density)

    # Find division connections
    connections = [div['connected_to'] for div in divisions_connection_data['divisions'] if div['name'] == name]

    return {
        "division_name": name,
        "area": area,
        "population_density": population_density,
        "land_use": allocations['land_use'],  # Ensure land_use is included
        "connections": connections[0] if connections else []
    }


# Function to distribute spatial planning generation using multiprocessing
def dcs_parallel_processing(divisions_gdf):
    division_data = [(row['name'], row['geometry'], random.randint(100, 1000)) for index, row in
                     divisions_gdf.iterrows()]

    with Pool(processes=4) as pool:
        results = pool.map(generate_spatial_plan, division_data)

    return results


# Function to simulate random partitioning of a division polygon
def create_organic_partition(geometry, allocations, buffer_dist=0.02):
    """Create organic partitions within the division polygon."""
    zones = {}
    minx, miny, maxx, maxy = geometry.bounds
    total_area = geometry.area

    remaining_geometry = geometry

    for zone, allocation in allocations.items():
        zone_area = allocation / total_area

        # Randomly generate points inside the division to create sub-zones
        num_points = max(5, int(zone_area * 100))  # More points for larger zones
        points = [Point(random.uniform(minx, maxx), random.uniform(miny, maxy)) for _ in range(num_points)]

        sub_zone_polygon = remaining_geometry.buffer(buffer_dist)

        # Ensure the area of the generated sub-zone matches the required allocation
        if sub_zone_polygon.area >= zone_area:
            zones[zone] = sub_zone_polygon
            remaining_geometry = remaining_geometry.difference(sub_zone_polygon)
        else:
            zones[zone] = remaining_geometry

    return zones


# Function to generate high-resolution images for each division's spatial plan
def generate_plan_images(divisions_gdf, spatial_plans):
    if divisions_gdf.empty:
        print("Error: Divisions GeoDataFrame is empty.")
        exit(1)

    # Plotting each division
    for idx, plan in enumerate(spatial_plans):
        division_name = plan['division_name']

        if idx < len(divisions_gdf):  # Ensure index is within bounds
            fig, ax = plt.subplots(figsize=(10, 10), dpi=300)  # Higher resolution (dpi=300)
            divisions_gdf.iloc[[idx]].plot(ax=ax, color="lightgray", edgecolor="black")

            # Check if geometry is valid
            geometry = divisions_gdf.iloc[idx].geometry if 'geometry' in divisions_gdf.columns else None
            if geometry is None:
                print(f"Error: No geometry found for division at index {idx}.")
                continue

            # Create organic partitioned polygons for different land use zones
            allocations = plan['land_use']  # Land use allocations from the spatial plan
            partitioned_zones = create_organic_partition(geometry, allocations)

            # Define colors for each zone type
            zone_colors = {
                "residential": "lightcoral",
                "agriculture": "lightgreen",
                "industrial": "lightblue",
                "green_space": "lightyellow"
            }

            # Plot each partitioned zone with a specific color
            for zone, polygon in partitioned_zones.items():
                if isinstance(polygon, MultiPolygon):  # Handle MultiPolygon
                    for p in polygon.geoms:  # Iterate over the individual Polygons
                        patch = PolygonPatch(p, facecolor=zone_colors[zone], edgecolor="black", alpha=0.5)
                        ax.add_patch(patch)
                elif isinstance(polygon, Polygon):  # Handle single Polygon
                    patch = PolygonPatch(polygon, facecolor=zone_colors[zone], edgecolor="black", alpha=0.5)
                    ax.add_patch(patch)

            # Add title and legend
            ax.set_title(f"Spatial Plan for {division_name}", fontsize=16)
            ax.legend(
                handles=[plt.Line2D([0], [0], color=color, lw=4, label=zone) for zone, color in zone_colors.items()])

            # Save each image as high-resolution PNG
            output_dir = "../../outputs"
            os.makedirs(output_dir, exist_ok=True)
            plt.savefig(f"{output_dir}/spatial_plan_{division_name}.png", dpi=300)  # Higher resolution
            plt.close()
        else:
            print(f"Error: Index {idx} out of range for divisions_gdf.")


if __name__ == "__main__":
    # Load the division contour (GeoJSON or shapefile)
    divisions_gdf = gpd.read_file('../../uploads/input_layers/contour.geojson')

    # Run the distributed spatial planning system
    spatial_plans = dcs_parallel_processing(divisions_gdf)

    # Generate spatial planning images for each division
    generate_plan_images(divisions_gdf, spatial_plans)
