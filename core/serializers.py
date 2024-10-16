# core/serializers.py
from rest_framework import serializers
from .models import Contour, Topography, EcoZone, AdministrativeBoundary, Infrastructure, Socioeconomic, DigitalGrid, TemporalEvolution
from .models import InfrastructureOutput, ZoningOutput, ProtectedAreasOutput, TransportationOutput, PopulationOutput, SocioeconomicOutput, UtilityOutput, TemporalEvolutionOutput

# Serializers for Input Layers
class ContourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contour
        fields = '__all__'

class TopographySerializer(serializers.ModelSerializer):
    class Meta:
        model = Topography
        fields = '__all__'

class EcoZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcoZone
        fields = '__all__'

class AdministrativeBoundarySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeBoundary
        fields = '__all__'

class InfrastructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infrastructure
        fields = '__all__'

class SocioeconomicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socioeconomic
        fields = '__all__'

class DigitalGridSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalGrid
        fields = '__all__'

class TemporalEvolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporalEvolution
        fields = '__all__'

# Serializers for Output Layers
class InfrastructureOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfrastructureOutput
        fields = '__all__'

class ZoningOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoningOutput
        fields = '__all__'

class ProtectedAreasOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtectedAreasOutput
        fields = '__all__'

class TransportationOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportationOutput
        fields = '__all__'

class PopulationOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopulationOutput
        fields = '__all__'

class SocioeconomicOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocioeconomicOutput
        fields = '__all__'

class UtilityOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilityOutput
        fields = '__all__'

class TemporalEvolutionOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporalEvolutionOutput
        fields = '__all__'
