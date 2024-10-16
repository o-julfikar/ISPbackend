"""
URL configuration for ISPbackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('contour/', views.ContourListCreate.as_view(), name='contour-list-create'),
    path('contour/<int:pk>/', views.ContourDetail.as_view(), name='contour-detail'),

    path('topography/', views.TopographyListCreate.as_view(), name='topography-list-create'),
    path('topography/<int:pk>/', views.TopographyDetail.as_view(), name='topography-detail'),

    path('ecozone/', views.EcoZoneListCreate.as_view(), name='ecozone-list-create'),
    path('ecozone/<int:pk>/', views.EcoZoneDetail.as_view(), name='ecozone-detail'),

    path('administrative-boundary/', views.AdministrativeBoundaryListCreate.as_view(), name='administrative-boundary-list-create'),
    path('administrative-boundary/<int:pk>/', views.AdministrativeBoundaryDetail.as_view(), name='administrative-boundary-detail'),

    path('infrastructure/', views.InfrastructureListCreate.as_view(), name='infrastructure-list-create'),
    path('infrastructure/<int:pk>/', views.InfrastructureDetail.as_view(), name='infrastructure-detail'),

    path('socioeconomic/', views.SocioeconomicListCreate.as_view(), name='socioeconomic-list-create'),
    path('socioeconomic/<int:pk>/', views.SocioeconomicDetail.as_view(), name='socioeconomic-detail'),

    path('digital-grid/', views.DigitalGridListCreate.as_view(), name='digital-grid-list-create'),
    path('digital-grid/<int:pk>/', views.DigitalGridDetail.as_view(), name='digital-grid-detail'),

    path('temporal-evolution/', views.TemporalEvolutionListCreate.as_view(), name='temporal-evolution-list-create'),
    path('temporal-evolution/<int:pk>/', views.TemporalEvolutionDetail.as_view(), name='temporal-evolution-detail'),

    # Output Layer URLs
    path('infrastructure-output/', views.InfrastructureOutputListCreate.as_view(), name='infrastructure-output-list-create'),
    path('infrastructure-output/<int:pk>/', views.InfrastructureOutputDetail.as_view(), name='infrastructure-output-detail'),

    path('zoning-output/', views.ZoningOutputListCreate.as_view(), name='zoning-output-list-create'),
    path('zoning-output/<int:pk>/', views.ZoningOutputDetail.as_view(), name='zoning-output-detail'),

    path('protected-areas-output/', views.ProtectedAreasOutputListCreate.as_view(), name='protected-areas-output-list-create'),
    path('protected-areas-output/<int:pk>/', views.ProtectedAreasOutputDetail.as_view(), name='protected-areas-output-detail'),

    path('transportation-output/', views.TransportationOutputListCreate.as_view(), name='transportation-output-list-create'),
    path('transportation-output/<int:pk>/', views.TransportationOutputDetail.as_view(), name='transportation-output-detail'),

    path('population-output/', views.PopulationOutputListCreate.as_view(), name='population-output-list-create'),
    path('population-output/<int:pk>/', views.PopulationOutputDetail.as_view(), name='population-output-detail'),

    path('socioeconomic-output/', views.SocioeconomicOutputListCreate.as_view(), name='socioeconomic-output-list-create'),
    path('socioeconomic-output/<int:pk>/', views.SocioeconomicOutputDetail.as_view(), name='socioeconomic-output-detail'),

    path('utility-output/', views.UtilityOutputListCreate.as_view(), name='utility-output-list-create'),
    path('utility-output/<int:pk>/', views.UtilityOutputDetail.as_view(), name='utility-output-detail'),

    path('temporal-evolution-output/', views.TemporalEvolutionOutputListCreate.as_view(), name='temporal-evolution-output-list-create'),
    path('temporal-evolution-output/<int:pk>/', views.TemporalEvolutionOutputDetail.as_view(), name='temporal-evolution-output-detail'),
    path('upload-geojson/', views.upload_geojson, name='upload_geojson'),
    path('get-avaialable-input-layers/', views.get_available_input_layers, name='get_available_input_layers'),
    path('spatial-planning/', views.spatialPlanning, name='spatial-planning'),
]
