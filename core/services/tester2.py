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
    public_space = area * 0.15  # 15% green space

    total_public_services = area * 0.1  # 10% for public services
    healthcare = total_public_services * 0.3
    education = total_public_services * 0.3
    admin = total_public_services * 0.4

    return {
        "land_use": {
            "residential": residential,
            "agriculture": agriculture,
            "industrial": industrial,
            "public_space": public_space
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
# def create_organic_partition(geometry, allocations, buffer_dist=-0.08):
#     """Create organic partitions within the division polygon."""
#     # print(allocations)
#     zones = {}
#     minx, miny, maxx, maxy = geometry.bounds
#     total_area = geometry.area
#     current_area = 0
# 
#     remaining_geometry = geometry
# 
#     for zone, allocation in allocations.items():
#         # Calculate the area for this zone
#         zone_area = allocation / total_area * remaining_geometry.area
#         # print("> ", allocation / total_area, allocation / total_area * remaining_geometry.area)
#         print("create_organic_partition:", zone, zone_area, allocation)
# 
#         # Randomly generate a few points inside the division to create sub-zones
#         num_points = max(5, int(zone_area * 100))  # More points for larger zones
#         # print(num_points)
#         points = [Point(random.uniform(minx, maxx), random.uniform(miny, maxy)) for _ in range(num_points)]
#         # print(points)
# 
#         # Create Voronoi-like partitioning or other partitioning from points
#         sub_zone_polygon = remaining_geometry.buffer(buffer_dist * zone_area / total_area)
#         # isp_voronoi_polygons = voronoi_diagram(points)
# 
# 
#         # sub_zone_polygon = None
#         # Ensure the area of the generated sub-zone matches the required allocation
#         if sub_zone_polygon.area >= zone_area:
#             print(">>> HAO!")
#             print(">>> ", remaining_geometry)
#             print("<<> ", sub_zone_polygon)
#             print("<>> ", sub_zone_polygon.intersection(remaining_geometry))
#             zones[zone] = sub_zone_polygon.intersection(remaining_geometry) # sub_zone_polygon
#             current_area += zone_area
#             remaining_geometry = remaining_geometry.difference(zones[zone])
#             print("><> ", remaining_geometry)
#         else:
#             zones[zone] = remaining_geometry
# 
# 
# 
#         # for poly in isp_voronoi_polygons.geoms:
#         #     if poly.intersects(remaining_geometry):
#         #         sub_zone_polygon = poly.intersects(remaining_geometry)
#         #         break
#         #
#         # if sub_zone_polygon and sub_zone_polygon.area >= zone_area:
#         #     zones[zone] = sub_zone_polygon
#         #     remaining_geometry = remaining_geometry.difference(sub_zone_polygon)
#         # else:
#         #     zones[zone] = remaining_geometry
# 
# 
# 
# 
#     print("create_organic_partition:", zones)
#     return zones

from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import voronoi_diagram


# def create_organic_partition(geometry, allocations, buffer_dist=-0.08):
#     """Create organic partitions within the division polygon."""
#     zones = {}
#     minx, miny, maxx, maxy = geometry.bounds
#     total_area = geometry.area
#     remaining_geometry = geometry
#
#     for zone, allocation in allocations.items():
#         # Calculate the area for this zone
#         zone_area = allocation / total_area * remaining_geometry.area
#
#         # Generate random points within the geometry
#         num_points = max(5, int(zone_area * 100))
#         points = [Point(random.uniform(minx, maxx), random.uniform(miny, maxy)) for _ in range(num_points)]
#
#         # Create Voronoi diagram based on points
#         vor = Voronoi([(p.x, p.y) for p in points])
#
#         # Partition using Voronoi cells
#         sub_zone_polygons = [Polygon(vor.vertices[region]) for region in vor.regions if
#                              region != -1 and len(region) > 0]
#
#         # Intersect polygons with the remaining geometry to ensure they fit
#         intersected_polygons = [poly.intersection(remaining_geometry) for poly in sub_zone_polygons if
#                                 poly.is_valid and poly.intersects(remaining_geometry)]
#
#         if intersected_polygons:
#             sub_zone_polygon = intersected_polygons[0]  # Choose the first valid intersection
#             if sub_zone_polygon.area >= zone_area:
#                 zones[zone] = sub_zone_polygon
#                 remaining_geometry = remaining_geometry.difference(sub_zone_polygon)
#             else:
#                 zones[zone] = remaining_geometry
#
#     return zones


def create_organic_partition(geometry, allocations, num_seeds_per_zone=None):
    """Create practical partitions of the given region."""

    if num_seeds_per_zone is None:
        num_seeds_per_zone = {
            'residential': 37,
            'agriculture': 21,
            'industrial': 11,
            'public_space': 18
        }

    zones = {}
    minx, miny, maxx, maxy = geometry.bounds

    zone_seeds = {
        'residential': [],
        'agriculture': [],
        'industrial': [],
        'public_space': []
    }

    # print(type(geometry), geometry)

    # Generate random seed points for each zone based on the number of required seeds
    for zone, num_seeds in num_seeds_per_zone.items():
        for _ in range(num_seeds):
            mock_point = None

            while not mock_point and not geometry.within(mock_point):
                mock_point = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))

            zone_seeds[zone].append(mock_point)

    # print(*[(k, v) for k, v in zone_seeds.items()], sep='\n')

    # Merge all seed points together for Voronoi diagram generation
    all_points = sum(zone_seeds.values(), [])

    # Create Voronoi diagram based on seed points
    # vor = voronoi_diagram(MultiPolygon(geometry), all_points)

    if isinstance(geometry, MultiPolygon):
        multi_points = np.array([p for poly in geometry.geoms for p in poly.exterior.coords])
    else:
        multi_points = np.array(geometry.exterior.coords)

    zone_points = {}

    for zone, zone_seed in zone_seeds.items():
        # print(zone_seed)
        # l = [p.coords[0] for p in zone_seed]
        # print(l)
        # print(l[0])
        # print(dir(l[0]))
        # print(l[0].xy)
        # print(l[0].coords)

        # return
        # print(zone_seed)
        if len(zone_seed) > 2:
            zone_points[zone] = Voronoi(np.array([p.coords[0] for p in zone_seed]))
            # print("done")
        # else:
            # print("WHY:", zone_seed)
        # zone_points[zone] = zone_seed

    vor = Voronoi(multi_points)

    # print(vor)
    # print(vor.points, type(vor.points), sep="\n")
    v_points = [Point(coord) for coord in vor.points]
    # print(v_points)
    # print(zone_seeds['residential'])

    # Assign Voronoi cells to zones
    for zone, points in zone_seeds.items():
        for pt in points:
            for cell in v_points:
                if pt.intersects(cell):
                    zones[zone] = cell
                    # print(" OOOO ", zones[zone])
                # else:
                    # print(pt, cell, sep=" <<>> ")
        if zone not in zones:
            zones[zone] = MultiPolygon([])
        # zones[zone] = MultiPolygon([cell for cell in v_points if any(pt.intersects(cell) for pt in points)])
        # print(">> Completed <<")

    # Adjust for industrial area isolation and residential/public access
    isolated_industrial_zones = []
    for industrial_area in zones['industrial'].geoms:
        buffer_zone = industrial_area.buffer(0.1)  # Buffer to isolate industrial zones
        agriculture_buffer = zones['agriculture'].difference(buffer_zone)
        isolated_industrial_zones.append(agriculture_buffer)

    zones['industrial'] = MultiPolygon(isolated_industrial_zones)

    # Return the zone polygons
    return zones, zone_points

# Function to generate high-resolution images for each division's spatial plan
# def generate_plan_images(divisions_gdf, spatial_plans):
#     for idx, plan in enumerate(spatial_plans):
#         # return
#
#         division_name = plan['division_name']
#
#         # Plot a blank map for visualization
#         fig, ax = plt.subplots(figsize=(10, 10), dpi=300)  # Higher resolution (dpi=300)
#         divisions_gdf.iloc[[idx]].plot(ax=ax, color="lightgray", edgecolor="black")
#         # ax.set_xlim(0, 10)
#         # ax.set_ylim(0, 10)
#         xlim = ax.get_xlim()
#         ylim = ax.get_ylim()
#         # Create organic partitioned polygons for different land use zones
#         geometry = divisions_gdf.iloc[idx].geometry
#         allocations = plan['allocations']['land_use']  # Land use allocations from the spatial plan
#         partitioned_zones, zone_points = create_organic_partition(geometry, allocations)
#
#         # Define colors for each zone type
#         zone_colors = {
#             "residential": "red",
#             "agriculture": "green",
#             "industrial": "blue",
#             "public_space": "orange"
#         }
#
#         for zone, zone_point in zone_points.items():
#             # print("plan", zone_point)
#             voronoi_plot_2d(zone_point, ax=ax, line_colors=zone_colors[zone])
#
#         ax.set_xlim(xlim)
#         ax.set_ylim(ylim)
#
#         # Plot each partitioned zone with a specific color
#         # print(len(partitioned_zones), type(partitioned_zones))
#         # print(partitioned_zones)
#
#         # for zone, polygon in partitioned_zones.items():
#         #     # print(zone)
#         #     # print("---")
#         #     # print(polygon)
#         #     # continue
#         #
#         #
#         #     if isinstance(polygon, MultiPolygon):
#         #         # print("> IS MULTIPLE POLYGON")
#         #         print("<< FIRST HERE")
#         #         print(zone, polygon)
#         #         for p in polygon.geoms:
#         #             # print(p)
#         #             # print(p.is_valid, p)
#         #             print(">> CHECK HERE")
#         #             if p.is_valid:
#         #                 patch = PolygonPatch(p, facecolor=zone_colors[zone], edgecolor="black", alpha=0.5)
#         #                 ax.add_patch(patch)
#         #             # else:
#         #                 # print(p)
#         #     else:
#         #         print(">> ELSE CHECK HERE")
#         #         if polygon.is_valid and not polygon.is_empty:
#         #             print(">> >> VALID")
#         #             patch = PolygonPatch(polygon, facecolor=zone_colors[zone], edgecolor="black", alpha=0.5)
#         #             ax.add_patch(patch)
#
#
#         # Add title and legend
#         ax.set_title(f"Spatial Plan for {division_name}", fontsize=16)
#         ax.legend(handles=[plt.Line2D([0], [0], color=color, lw=4, label=zone) for zone, color in zone_colors.items()])
#
#         # Create output directory if it doesn't exist
#         output_dir = "../../outputs"
#         os.makedirs(output_dir, exist_ok=True)
#
#         # Save each image as high-resolution PNG
#         plt.savefig(f"{output_dir}/spatial_plan_{division_name}.png", dpi=300)  # Higher resolution
#         plt.close()

from shapely.geometry import Point


def generate_plan_images(divisions_gdf, spatial_plans):
    for idx, plan in enumerate(spatial_plans):
        division_name = plan['division_name']

        # Plot a blank map for visualization
        fig, ax = plt.subplots(figsize=(10, 10), dpi=300)  # Higher resolution (dpi=300)
        divisions_gdf.iloc[[idx]].plot(ax=ax, color="lightgray", edgecolor="black")

        # Store current limits before plotting Voronoi
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        # Create organic partitioned polygons for different land use zones
        geometry = divisions_gdf.iloc[idx].geometry
        allocations = plan['allocations']['land_use']  # Land use allocations from the spatial plan
        partitioned_zones, zone_points = create_organic_partition(geometry, allocations)

        # Define colors for each zone type
        zone_colors = {
            "residential": "red",
            "agriculture": "green",
            "industrial": "blue",
            "public_space": "orange"
        }

        for zone, zone_point in zone_points.items():
            # Filter Voronoi points that are within the polygon
            temp_points = [p for p in zone_point.points]
            valid_zone_points = [point for point in temp_points if geometry.contains(Point(point))]

            if valid_zone_points:
                # Only plot if there are valid points
                xvor = Voronoi(valid_zone_points)
                voronoi_plot_2d(xvor, ax=ax, line_colors=zone_colors[zone])

        # Restore the axes limits
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

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
