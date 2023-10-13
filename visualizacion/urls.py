from django.urls import path
from . import views

urlpatterns = [
    path('', views.visualizacion, name='visualizacion'),
    path('get_departamento_ciudad_barrio/', views.get_departamento_ciudad_barrio),
    path('bienvenida/',views.bienvenida_visualizaciones, name='bienvenida_visualizaciones'),
    path('visualiza_covid/',views.visualiza_covid, name='visualiza_covid'),
    path('visualiza_dengue/',views.visualiza_dengue, name='visualiza_dengue'),
    path('visualiza_VIH/',views.visualiza_VIH, name='visualiza_VIH'),
]
