import os
from datetime import datetime
from timeit import timeit
import pyproj
import matplotlib.pyplot as plt
import geopandas as gpd
import random
from multiprocessing import Pool
import numpy as np
import shapely
from django.contrib.admin.templatetags.admin_list import results
from django.http import JsonResponse
from pyparsing import replaceWith
from shapely.geometry import Point
from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import Polygon, MultiPolygon




# Mock ML/AI function to allocate zones
def zone_allocation(area, population_density):
    """Assign land use zoning and public services based on area and population."""
    residential = area * 0.3  # 30% residential
    agriculture = area * 0.35  # 35% agricultural
    industrial = area * 0.2  # 20% industrial
    public_space = area * 0.15  # 15% public services

    total_public_services = public_space  # 10% for public services
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
        "public_space": {
            "total_public_services": total_public_services,
            "healthcare": healthcare,
            "education": education,
            "admin": admin
        }
    }


# Function to generate spatial planning for each division
def generate_spatial_plan(division_data, gdf_file):

    # if type(division_data) == list:
    #     division_data, gdf_file = division_data
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

    plan_data = {
        "division_name": name,
        "area": area,
        "population_density": population_density,
        "allocations": allocations,
        "connections": connections[0] if connections else []
    }

    generate_plan_images(gdf_file, [plan_data])

    return plan_data


# Function to distribute spatial planning generation
def dcs_parallel_processing(divisions_gdf, dcs_enabled=True):
    print("Process start...:", datetime.now())
    if dcs_enabled:
        division_data = [[(row['name'], row['geometry'], random.randint(100, 1000)), divisions_gdf] for index, row in
                         divisions_gdf.iterrows()]

        with Pool(processes=min(10, len(divisions_gdf))) as pool:
            spatial_results = pool.starmap(generate_spatial_plan, division_data)
    else:
        division_data = [(row['name'], row['geometry'], random.randint(100, 1000)) for index, row in
                     divisions_gdf.iterrows()]
        spatial_results = [generate_spatial_plan(division, divisions_gdf) for division in division_data]

    print("Process end...:", datetime.now())

    return spatial_results


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


    # Generate random seed points for each zone based on the number of required seeds
    for zone, num_seeds in num_seeds_per_zone.items():
        for _ in range(num_seeds):
            mock_point = None

            while not mock_point and not geometry.within(mock_point):
                mock_point = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))

            zone_seeds[zone].append(mock_point)

    all_points = sum(zone_seeds.values(), [])

    if isinstance(geometry, MultiPolygon):
        multi_points = np.array([p for poly in geometry.geoms for p in poly.exterior.coords])
    else:
        multi_points = np.array(geometry.exterior.coords)

    zone_points = {}

    for zone, zone_seed in zone_seeds.items():
        if len(zone_seed) > 2:
            zone_points[zone] = Voronoi(np.array([p.coords[0] for p in zone_seed]))

    vor = Voronoi(multi_points)

    v_points = [Point(coord) for coord in vor.points]

    # Assign Voronoi cells to zones
    for zone, points in zone_seeds.items():
        for pt in points:
            for cell in v_points:
                if pt.intersects(cell):
                    zones[zone] = cell
        if zone not in zones:
            zones[zone] = MultiPolygon([])

    # Adjust for industrial area isolation and residential/public access
    isolated_industrial_zones = []
    for industrial_area in zones['industrial'].geoms:
        buffer_zone = industrial_area.buffer(0.1)  # Buffer to isolate industrial zones
        agriculture_buffer = zones['agriculture'].difference(buffer_zone)
        isolated_industrial_zones.append(agriculture_buffer)

    zones['industrial'] = MultiPolygon(isolated_industrial_zones)

    # Return the zone polygons
    return zones, zone_points




def generate_plan_images(divisions_gdf, spatial_plans):
    for idx, plan in enumerate(spatial_plans):
        division_name = plan['division_name']

        # Plot a blank map for visualization
        fig, ax = plt.subplots(figsize=(10, 10), dpi=300)  # Higher resolution (dpi=300)

        geometry = divisions_gdf.iloc[idx].geometry
        for i, row in divisions_gdf.iterrows():
            if row["name"] == division_name:
                divisions_gdf.iloc[[i]].plot(ax=ax, color="lightgray", edgecolor="black")
                geometry = divisions_gdf.iloc[i].geometry

        # Store current limits before plotting Voronoi
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        # Create organic partitioned polygons for different land use zones
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
        output_dir = "media/outputs"
        os.makedirs(output_dir, exist_ok=True)

        # Save each image as high-resolution PNG
        plt.savefig(f"{output_dir}/spatial_plan_{division_name}.png", dpi=300)  # Higher resolution
        plt.close()


def get_spatial_planning_data(request):
    if request.method == "GET":
        contour_dir = 'uploads/input_layers/contour.geojson'

        if os.path.exists(contour_dir):
            contour_file = gpd.read_file(contour_dir)
            # print(contour_file.crs.is_geographic)

            if contour_file.crs.is_geographic:
                contour_file = contour_file.to_crs(epsg=32645)

            # print("HOL")
            # print("Bangladesh:", sum(contour_file.area / 1_000_000))
            # print("LA")
            spatial_plans_data = {v["division_name"]: v for v in dcs_parallel_processing(contour_file, dcs_enabled=True)}
            # generate_plan_images(contour_file, spatial_plans_data)

            spatial_plan_images = {}
            land_use_per_division = {}

            for plan in os.listdir("media/outputs/"):
                division = plan.split('.')[0].split('_')[-1]
                image_path = f"media/outputs/{plan}"
                land_use_data = {"residential": None, "agriculture": None, "industrial": None, "public_services": None, "public_space": None}

                # Make sure to create a full URL
                spatial_plan_images[division] = request.build_absolute_uri(f'/{image_path}')
                for k, v in spatial_plans_data[division]["allocations"]["land_use"].items():
                    land_use_data[k] = round(v / 1000000, 2)

                land_use_data['public_space'] = spatial_plans_data[division]["allocations"]["public_space"]

                for k, v in land_use_data['public_space'].items():
                    if k == "total_public_services":
                        land_use_data["public_services"] = round(v / 1_000_000, 2);
                    else:
                        land_use_data['public_space'][k] = round(v / 1000000, 2)

                del spatial_plans_data[division]["allocations"]["public_space"]["total_public_services"]



                land_use_per_division[division] = land_use_data


                # print(land_use_data)

            return JsonResponse({"spatial_plan_images": spatial_plan_images, "land_use": land_use_per_division}, status=200)

        return JsonResponse({"error": "Contour file not found"}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)

if __name__ == "__main__":
    divisions_gdf = gpd.read_file('../../uploads/input_layers/contour.geojson')

    # Run the distributed spatial planning system
    spatial_plans = dcs_parallel_processing(divisions_gdf)

    # Generate spatial planning images for each division
    generate_plan_images(divisions_gdf, spatial_plans)

