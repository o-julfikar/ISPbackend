import os
import random
import geopandas as gpd
from shapely.geometry import Point, Polygon, LineString
from multiprocessing import Pool
import matplotlib.pyplot as plt
import os
import random
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

import os
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon, Point
import random

import os
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon, Point, MultiPolygon
import random
import numpy as np
from descartes import PolygonPatch
from shapely.lib import voronoi_polygons
from shapely.ops import voronoi_diagram

divisions_gdf = gpd.read_file('../../uploads/input_layers/contour.geojson')

from multiprocessing import Pool


# Mock ML/AI function to allocate zones
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
            # Add other divisions here as needed
        ]
    }

    allocations = zone_allocation(area, population_density)

    connections = [div['connected_to'] for div in divisions_connection_data['divisions'] if div['name'] == name]

    return {
        "division_name": name,
        "area": area,
        "population_density": population_density,
        "allocations": allocations,
        "connections": connections[0] if connections else []
    }


# Function to distribute spatial planning generation
def dcs_parallel_processing(divisions_gdf):
    division_data = [(row['name'], row['geometry'], random.randint(100, 1000)) for index, row in
                     divisions_gdf.iterrows()]

    with Pool(processes=4) as pool:
        results = pool.map(generate_spatial_plan, division_data)

    return results



# Function to simulate random partitioning of a division polygon
def create_organic_partition(geometry, allocations, buffer_dist=0.02):
    """Create organic partitions within the division polygon."""
    # print(allocations)
    zones = {}
    minx, miny, maxx, maxy = geometry.bounds
    total_area = geometry.area
    current_area = 0

    remaining_geometry = geometry

    for zone, allocation in allocations.items():
        # Calculate the area for this zone
        zone_area = allocation / total_area * remaining_geometry.area
        # print("> ", allocation / total_area, allocation / total_area * remaining_geometry.area)
        print("create_organic_partition:", zone, zone_area, allocation)

        # Randomly generate a few points inside the division to create sub-zones
        num_points = max(5, int(zone_area * 100))  # More points for larger zones
        # print(num_points)
        points = [Point(random.uniform(minx, maxx), random.uniform(miny, maxy)) for _ in range(num_points)]
        # print(points)

        # Create Voronoi-like partitioning or other partitioning from points
        sub_zone_polygon = remaining_geometry.buffer(buffer_dist)
        # isp_voronoi_polygons = voronoi_diagram(points)


        # sub_zone_polygon = None
        # Ensure the area of the generated sub-zone matches the required allocation
        if sub_zone_polygon.area >= zone_area:
            print(">>> HAO!")
            print(">>> ", remaining_geometry)
            print("<<> ", sub_zone_polygon)
            print("<>> ", sub_zone_polygon.intersection(remaining_geometry))
            zones[zone] = sub_zone_polygon.intersection(remaining_geometry) # sub_zone_polygon
            current_area += zone_area
            remaining_geometry = remaining_geometry.difference(zones[zone])
            print("><> ", remaining_geometry)
        else:
            zones[zone] = remaining_geometry



        # for poly in isp_voronoi_polygons.geoms:
        #     if poly.intersects(remaining_geometry):
        #         sub_zone_polygon = poly.intersects(remaining_geometry)
        #         break
        #
        # if sub_zone_polygon and sub_zone_polygon.area >= zone_area:
        #     zones[zone] = sub_zone_polygon
        #     remaining_geometry = remaining_geometry.difference(sub_zone_polygon)
        # else:
        #     zones[zone] = remaining_geometry




    print("create_organic_partition:", zones)
    return zones


# Function to generate high-resolution images for each division's spatial plan
def generate_plan_images(divisions_gdf, spatial_plans):
    for idx, plan in enumerate(spatial_plans):
        # return

        division_name = plan['division_name']

        # Plot a blank map for visualization
        fig, ax = plt.subplots(figsize=(10, 10), dpi=300)  # Higher resolution (dpi=300)
        divisions_gdf.iloc[[idx]].plot(ax=ax, color="lightgray", edgecolor="black")

        # Create organic partitioned polygons for different land use zones
        geometry = divisions_gdf.iloc[idx].geometry
        allocations = plan['allocations']['land_use']  # Land use allocations from the spatial plan
        partitioned_zones = create_organic_partition(geometry, allocations)

        # Define colors for each zone type
        zone_colors = {
            "residential": "lightcoral",
            "agriculture": "lightgreen",
            "industrial": "lightblue",
            "green_space": "lightyellow"
        }

        # Plot each partitioned zone with a specific color
        # print(len(partitioned_zones), type(partitioned_zones))
        # print(partitioned_zones)

        for zone, polygon in partitioned_zones.items():
            # print(zone)
            # print("---")
            # print(polygon)
            # continue


            if isinstance(polygon, MultiPolygon):
                # print("> IS MULTIPLE POLYGON")
                for p in polygon.geoms:
                    # print(p)
                    # print(p.is_valid, p)
                    if p.is_valid:
                        patch = PolygonPatch(p, facecolor=zone_colors[zone], edgecolor="black", alpha=0.5)
                        ax.add_patch(patch)
                    # else:
                        # print(p)
            else:
                if polygon.is_valid and not polygon.is_empty:
                    patch = PolygonPatch(polygon, facecolor=zone_colors[zone], edgecolor="black", alpha=0.5)
                    ax.add_patch(patch)


        # Add title and legend
        ax.set_title(f"Spatial Plan for {division_name}", fontsize=16)
        ax.legend(handles=[plt.Line2D([0], [0], color=color, lw=4, label=zone) for zone, color in zone_colors.items()])

        # Create output directory if it doesn't exist
        output_dir = "../../outputs"
        os.makedirs(output_dir, exist_ok=True)

        # Save each image as high-resolution PNG
        plt.savefig(f"{output_dir}/spatial_plan_{division_name}.png", dpi=300)  # Higher resolution
        plt.close()


if __name__ == "__main__":
    # Load the division contour (GeoJSON or shapefile)
    # divisions_gdf = gpd.read_file('path_to_division_contours.geojson')

    # Run the distributed spatial planning system
    spatial_plans = dcs_parallel_processing(divisions_gdf)

    # Generate spatial planning images for each division
    generate_plan_images(divisions_gdf, spatial_plans)

    # divisions_connection_data = {
    #     "divisions": [
    #         {
    #             "name": "Barishal",
    #             "connected_to": ["Dhaka", "Khulna"]
    #         },
    #         {
    #             "name": "Chittagong",
    #             "connected_to": ["Dhaka", "Sylhet"]
    #         },
    #         # Add other divisions here as needed
    #     ]
    # }
