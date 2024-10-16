from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework import generics
from .serializers import *
import geopandas as gpd
import random
import os

import psutil


def index(request):
    return render(request, 'core/index.html')

def spatialPlanning(request):
    return render(request, 'core/spatial_planning_dcs.html')

@csrf_exempt
def upload_geojson(request):
    if request.method == 'POST':
        # Check if any files are uploaded
        print("Hel")
        if not request.FILES:
            return JsonResponse({'error': 'No files uploaded.'}, status=400)

        # Create a directory to store the uploaded files if it doesn't exist
        os.makedirs('uploads/input_layers', exist_ok=True)

        for file_key, uploaded_file in request.FILES.items():
            # Process each uploaded file
            if uploaded_file.name.endswith('.geojson') or uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.json'):
                # Save the file temporarily
                ext = uploaded_file.name.split('.')[-1]
                with open(f'uploads/input_layers/{file_key}.{ext}', 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
            else:
                return JsonResponse({'error': f'Invalid file format for {uploaded_file.name}. Please upload a valid file.'}, status=400)

        return JsonResponse({'message': 'Files uploaded successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid request method. Only POST allowed.'}, status=405)


@csrf_exempt
def get_available_input_layers(request):
    if request.method == "GET":
        layers = []
        directory = "uploads/input_layers/"  # Directory where GeoJSON files are stored

        # Check if the directory exists
        if os.path.exists(directory):
            # List all files in the directory
            for file_name in os.listdir(directory):
                # Only add files with .geojson extension
                if file_name.endswith(".geojson"):
                    layers.append(file_name.split(".")[0])

        # Return the list of geojson files as JSON response
        return JsonResponse({"layers": layers})

    return JsonResponse({"error": "Method Not Allowed. Only GET allowed."}, status=405)

# Input Layer Views

def get_spatial_plan(request):
    if request.method == "GET":
        # Load contour GeoJSON file from directory
        contour_file_path = os.path.join("uploads/input_layers/", "contour.geojson")
        contour_data = load_contour_geojson(contour_file_path)

        if contour_data is None:
            return JsonResponse({"error": "Contour data not found"}, status=404)

        # Generate population density
        population_density = generate_population_density(contour_data)

        # Create spatial plan
        spatial_plan = create_spatial_plan(contour_data, population_density)

        return JsonResponse(spatial_plan, safe=False)

    return JsonResponse({"error": "Method not allowed"}, status=405)

def load_contour_geojson(file_path):
    try:
        contour_data = gpd.read_file(file_path)
        return contour_data
    except Exception as e:
        print(f"Error loading contour file: {e}")
        return None

def generate_population_density(contour_data):
    population_density = {}
    for i, region in enumerate(contour_data['geometry']):
        population_density[f"Region-{i + 1}"] = random.randint(500, 5000)
    return population_density

def create_spatial_plan(contour_data, population_density):
    spatial_plan = {}
    for i, region in enumerate(contour_data['geometry']):
        region_name = f"Region-{i + 1}"
        population = population_density.get(region_name, 1000)
        if population < 1000:
            planning_type = "Green Space"
        elif 1000 <= population < 3000:
            planning_type = "Residential Area"
        elif 3000 <= population < 4500:
            planning_type = "Commercial Area"
        else:
            planning_type = "Infrastructure Development"

        spatial_plan[region_name] = {
            "population_density": population,
            "suggested_use": planning_type
        }
    return spatial_plan


class ContourListCreate(generics.ListCreateAPIView):
    queryset = Contour.objects.all()
    serializer_class = ContourSerializer

class ContourDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contour.objects.all()
    serializer_class = ContourSerializer

class TopographyListCreate(generics.ListCreateAPIView):
    queryset = Topography.objects.all()
    serializer_class = TopographySerializer

class TopographyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topography.objects.all()
    serializer_class = TopographySerializer

class EcoZoneListCreate(generics.ListCreateAPIView):
    queryset = EcoZone.objects.all()
    serializer_class = EcoZoneSerializer

class EcoZoneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EcoZone.objects.all()
    serializer_class = EcoZoneSerializer

class AdministrativeBoundaryListCreate(generics.ListCreateAPIView):
    queryset = AdministrativeBoundary.objects.all()
    serializer_class = AdministrativeBoundarySerializer

class AdministrativeBoundaryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdministrativeBoundary.objects.all()
    serializer_class = AdministrativeBoundarySerializer

class InfrastructureListCreate(generics.ListCreateAPIView):
    queryset = Infrastructure.objects.all()
    serializer_class = InfrastructureSerializer

class InfrastructureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Infrastructure.objects.all()
    serializer_class = InfrastructureSerializer

class SocioeconomicListCreate(generics.ListCreateAPIView):
    queryset = Socioeconomic.objects.all()
    serializer_class = SocioeconomicSerializer

class SocioeconomicDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Socioeconomic.objects.all()
    serializer_class = SocioeconomicSerializer

class DigitalGridListCreate(generics.ListCreateAPIView):
    queryset = DigitalGrid.objects.all()
    serializer_class = DigitalGridSerializer

class DigitalGridDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DigitalGrid.objects.all()
    serializer_class = DigitalGridSerializer

class TemporalEvolutionListCreate(generics.ListCreateAPIView):
    queryset = TemporalEvolution.objects.all()
    serializer_class = TemporalEvolutionSerializer

class TemporalEvolutionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TemporalEvolution.objects.all()
    serializer_class = TemporalEvolutionSerializer

# Output Layer Views

class InfrastructureOutputListCreate(generics.ListCreateAPIView):
    queryset = InfrastructureOutput.objects.all()
    serializer_class = InfrastructureOutputSerializer

class InfrastructureOutputDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = InfrastructureOutput.objects.all()
    serializer_class = InfrastructureOutputSerializer

class ZoningOutputListCreate(generics.ListCreateAPIView):
    queryset = ZoningOutput.objects.all()
    serializer_class = ZoningOutputSerializer

class ZoningOutputDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ZoningOutput.objects.all()
    serializer_class = ZoningOutputSerializer

class ProtectedAreasOutputListCreate(generics.ListCreateAPIView):
    queryset = ProtectedAreasOutput.objects.all()
    serializer_class = ProtectedAreasOutputSerializer

class ProtectedAreasOutputDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProtectedAreasOutput.objects.all()
    serializer_class = ProtectedAreasOutputSerializer

class TransportationOutputListCreate(generics.ListCreateAPIView):
    queryset = TransportationOutput.objects.all()
    serializer_class = TransportationOutputSerializer

class TransportationOutputDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TransportationOutput.objects.all()
    serializer_class = TransportationOutputSerializer

class PopulationOutputListCreate(generics.ListCreateAPIView):
    queryset = PopulationOutput.objects.all()
    serializer_class = PopulationOutputSerializer

class PopulationOutputDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PopulationOutput.objects.all()
    serializer_class = PopulationOutputSerializer

class SocioeconomicOutputListCreate(generics.ListCreateAPIView):
    queryset = SocioeconomicOutput.objects.all()
    serializer_class = SocioeconomicOutputSerializer

class SocioeconomicOutputDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SocioeconomicOutput.objects.all()
    serializer_class = SocioeconomicOutputSerializer

class UtilityOutputListCreate(generics.ListCreateAPIView):
    queryset = UtilityOutput.objects.all()
    serializer_class = UtilityOutputSerializer

class UtilityOutputDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UtilityOutput.objects.all()
    serializer_class = UtilityOutputSerializer

class TemporalEvolutionOutputListCreate(generics.ListCreateAPIView):
    queryset = TemporalEvolutionOutput.objects.all()
    serializer_class = TemporalEvolutionOutputSerializer

class TemporalEvolutionOutputDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TemporalEvolutionOutput.objects.all()
    serializer_class = TemporalEvolutionOutputSerializer
