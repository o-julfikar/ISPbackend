from django.db import models

# Contour Layer Model
class Contour(models.Model):
    contour_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    area = models.FloatField()  # Total area of the contour
    coordinates = models.JSONField()  # List of coordinates representing the boundary (latitude, longitude)

    def __str__(self):
        return self.name

# Topography Layer Model
class Topography(models.Model):
    topography_id = models.AutoField(primary_key=True)
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE)
    elevation = models.FloatField()  # Elevation in meters
    terrain = models.CharField(max_length=100)
    coordinates = models.JSONField()  # Location-specific topography data

    def __str__(self):
        return f'Topography for {self.contour.name}'

# EcoZone Layer Model
class EcoZone(models.Model):
    ecozone_id = models.AutoField(primary_key=True)
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    area_covered = models.FloatField()
    protection_level = models.CharField(max_length=100)
    coordinates = models.JSONField()  # Ecozone area coordinates

    def __str__(self):
        return f'EcoZone in {self.contour.name}'

# Administrative Boundaries Model
class AdministrativeBoundary(models.Model):
    boundary_id = models.AutoField(primary_key=True)
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE)
    admin_type = models.CharField(max_length=100)
    coordinates = models.JSONField()  # Boundaries represented by coordinates

    def __str__(self):
        return f'Administrative Boundary in {self.contour.name}'

# Infrastructure Layer Model
class Infrastructure(models.Model):
    infrastructure_id = models.AutoField(primary_key=True)
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)  # Road, building, etc.
    infrastructure_condition = models.CharField(max_length=100)
    coordinates = models.JSONField()  # Position of the infrastructure within the contour

    def __str__(self):
        return f'{self.type} in {self.contour.name}'

# Socioeconomic Layer Model
class Socioeconomic(models.Model):
    socioeconomic_id = models.AutoField(primary_key=True)
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE)
    density = models.IntegerField()  # Population density
    distribution = models.CharField(max_length=100)
    age_demographics = models.CharField(max_length=100)
    coordinates = models.JSONField()  # Distribution points of population

    def __str__(self):
        return f'Socioeconomic data for {self.contour.name}'

# Digital Grid Layer Model
class DigitalGrid(models.Model):
    digital_grid_id = models.AutoField(primary_key=True)
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE)
    power_capacity = models.IntegerField()
    coverage_area = models.FloatField()
    coordinates = models.JSONField()  # Coverage area coordinates for grid

    def __str__(self):
        return f'Digital Grid in {self.contour.name}'

# Temporal Evolution Layer Model
class TemporalEvolution(models.Model):
    temporal_id = models.AutoField(primary_key=True)
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE)
    year = models.IntegerField()
    event_type = models.CharField(max_length=100)
    description = models.TextField()
    coordinates = models.JSONField()  # Specific area affected

    def __str__(self):
        return f'Temporal event {self.event_type} in {self.contour.name}'


#################### OUTPUT LAYERS #########################

# Infrastructure Layer
class InfrastructureOutput(models.Model):
    infrastructure_output_id = models.AutoField(primary_key=True)
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE)
    infrastructure_type = models.CharField(max_length=100)  # e.g., Road, Building, Utility
    proposed_condition = models.CharField(max_length=100)  # e.g., New, Refurbished
    coordinates = models.JSONField()  # Store infrastructure placement coordinates
    capacity = models.FloatField()  # Capacity for new infrastructure (if applicable)
    construction_year = models.IntegerField()  # Planned construction year

# Zoning and Lang Use Layer
class ZoningOutput(models.Model):
    zoning_output_id = models.AutoField(primary_key=True)
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE)
    zoning_type = models.CharField(max_length=100)  # e.g., Residential, Commercial, Green Space
    coordinates = models.JSONField()  # Coordinates of the zoned area
    proposed_capacity = models.IntegerField()  # Proposed population or usage capacity
    regulations = models.TextField()  # Proposed regulations or restrictions

# Protected Areas (EcoZone) Layer
class ProtectedAreasOutput(models.Model):
    protected_area_id = models.AutoField(primary_key=True)
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE)
    protection_type = models.CharField(max_length=100)  # e.g., National Park, Wildlife Reserve
    area_covered = models.FloatField()  # Area in square kilometers
    coordinates = models.JSONField()  # Geographic boundaries
    protection_level = models.CharField(max_length=100)  # Level of protection (e.g., High, Medium)

# Transportation Output Layer
class TransportationOutput(models.Model):
    transport_output_id = models.AutoField(primary_key=True)
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE)
    transport_type = models.CharField(max_length=100)  # e.g., Road, Railway, Highway
    road_length = models.FloatField()  # Proposed road/rail length
    coordinates = models.JSONField()  # Coordinates for the new network
    traffic_density = models.CharField(max_length=100)  # Predicted traffic density

# Population and Socioeconomic Output Layer
class PopulationOutput(models.Model):
    population_id = models.AutoField(primary_key=True)
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE)
    total_population = models.IntegerField()
    density = models.FloatField()
    distribution = models.CharField(max_length=100)
    age_demographics = models.CharField(max_length=100)
    growth_rate = models.FloatField()
    migration_patterns = models.TextField()

    def __str__(self):
        return f"Population data for {self.contour.name}"

class SocioeconomicOutput(models.Model):
    socioeconomic_id = models.AutoField(primary_key=True)
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE)
    income_levels = models.CharField(max_length=100)
    employment_rate = models.FloatField()
    poverty_rate = models.FloatField()
    education_levels = models.TextField()
    healthcare_access = models.CharField(max_length=100)
    median_income = models.FloatField()

    def __str__(self):
        return f"Socioeconomic data for {self.contour.name}"


#Utility and Digital Infrastructure Output Layer
class UtilityOutput(models.Model):
    utility_output_id = models.AutoField(primary_key=True)
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE)
    utility_type = models.CharField(max_length=100)  # e.g., Power, Water, Internet
    coverage_area = models.FloatField()  # Area covered by the utility
    capacity = models.FloatField()  # Capacity of the utility
    coordinates = models.JSONField()  # Locations of utility infrastructure

# Temporal Evolution Output Layer
class TemporalEvolutionOutput(models.Model):
    temporal_output_id = models.AutoField(primary_key=True)
    contour = models.ForeignKey(Contour, on_delete=models.CASCADE)
    year = models.IntegerField()  # Year for the forecast or historical change
    forecasted_event = models.CharField(max_length=255)  # e.g., Population increase, Urbanization
    impact_description = models.TextField()  # Description of the predicted impact
    coordinates = models.JSONField()  # Location-specific changes
